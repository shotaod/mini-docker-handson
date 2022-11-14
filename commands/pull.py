import json
import os
import shutil
import tarfile
from typing import Iterable

import requests

import commands.config as config
import commands.format as fmt


def _fetch_auth_token(library: str, image: str) -> str:
    token_url = f'https://auth.docker.io/token?service=registry.docker.io&scope=repository:{library}/{image}:pull'
    token_response = requests.get(token_url)
    token_response.raise_for_status()
    return token_response.json()['token']


def _fetch_manifest(library: str, image: str, tag: str, token: str) -> dict:
    print(f'Fetching manifest for {image}:{tag}')
    manifest_url = f'{config.REGISTRY_BASE}/{library}/{image}/manifests/{tag}'
    headers = {'Authorization': f'Bearer {token}'}
    manifest_response = requests.get(manifest_url, headers=headers)
    manifest_response.raise_for_status()
    return manifest_response.json()


def _fetch_layer(library: str, image: str, layer_digest: str, token: str) -> Iterable[bytes]:
    print(f'Fetching layer: {layer_digest}')
    layer_url = f'{config.REGISTRY_BASE}/{library}/{image}/blobs/{layer_digest}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(layer_url, stream=True, headers=headers)
    response.raise_for_status()
    for chunk in response.iter_content(chunk_size=1024 * 8):
        if chunk:
            yield chunk


def exec_pull():
    print(f'pull command called!')
    return

    registry, image, tag = fmt.parse_image_opt(image_name)
    print(f'pulling {registry}/{image}:{tag} ...')

    # Docker Hub からアクセストークンを取得
    # See also: https://docs.docker.com/registry/spec/auth/jwt/
    token = _fetch_auth_token(registry, image)

    if not os.path.exists(config.IMAGE_DIR):
        os.makedirs(config.IMAGE_DIR)

    # 指定した Docker image のマニフェストを取得して保存
    # See also: https://docs.docker.com/registry/spec/manifest-v2-2/
    manifest = _fetch_manifest(registry, image, tag, token)

    image_name = f"{manifest['name'].replace('/', '_')}_{manifest['tag']}"
    image_base_dir = os.path.join(config.IMAGE_DIR, image_name)
    if os.path.exists(image_base_dir):
        shutil.rmtree(image_base_dir)
    if not os.path.exists(image_base_dir):
        os.makedirs(image_base_dir)

    with open(os.path.join(image_base_dir, 'manifest.json'), 'w') as manifest_file:
        json_txt = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True, separators=(',', ': '))
        manifest_file.write(json_txt)

    # Docker image を構成する各イメージ・レイヤを取得して保存
    # See also: https://qiita.com/zembutsu/items/24558f9d0d254e33088f
    layer_digests = [layer['blobSum'] for layer in manifest['fsLayers']]
    image_layers_path = os.path.join(image_base_dir, 'layers')
    contents_path = os.path.join(image_base_dir, 'contents')
    if not os.path.exists(image_layers_path):
        os.makedirs(image_layers_path)
    if not os.path.exists(contents_path):
        os.makedirs(contents_path)

    for digest in layer_digests:
        # layerごとに保存
        layer_tar_name = f'{os.path.join(image_layers_path, digest)}.tar'
        with open(layer_tar_name, 'wb') as tar:
            for chunk in _fetch_layer(registry, image, digest, token):
                if chunk:
                    tar.write(chunk)
        # ファイルは統合する
        with tarfile.open(layer_tar_name, 'r') as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, str(contents_path))

    print(f'👌 {fmt.GREEN}Docker image {image}:{tag} has been stored in {image_base_dir}{fmt.END}')
