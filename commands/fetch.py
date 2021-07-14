from typing import Iterable

import requests

import commands.config as cfg


def fetch_auth_token(library: str, image: str) -> str:
    print(f'Fetching auth token for {library}/{image}')
    token_url = f'{cfg.TOKEN_BASE}?service=registry.docker.io&scope=repository:{library}/{image}:pull'
    token_response = requests.get(token_url)
    token_response.raise_for_status()
    return token_response.json()['token']


def fetch_manifest(library: str, image: str, tag: str, token: str) -> dict:
    print(f'Fetching manifest for {image}:{tag}')
    manifest_url = f'{cfg.REGISTRY_BASE}/{library}/{image}/manifests/{tag}'
    headers = {'Authorization': f'Bearer {token}'}
    manifest_response = requests.get(manifest_url, headers=headers)
    manifest_response.raise_for_status()
    return manifest_response.json()


def fetch_layer(library: str, image: str, layer_digest: str, token: str) -> Iterable[bytes]:
    print(f'Fetching layer: {layer_digest}')
    layer_url = f'{cfg.REGISTRY_BASE}/{library}/{image}/blobs/{layer_digest}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(layer_url, stream=True, headers=headers)
    response.raise_for_status()
    for chunk in response.iter_content(chunk_size=1024 * 8):
        if chunk:
            yield chunk
