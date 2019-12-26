import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                pokemon.title, request.build_absolute_uri(pokemon.picture.url))

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.picture.url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)

    if pokemon_entities:
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                requested_pokemon.title, request.build_absolute_uri(requested_pokemon.picture.url))

    pokemon = {
        'img_url': request.build_absolute_uri(requested_pokemon.picture.url),
        'title_ru': requested_pokemon.title,
        'description': requested_pokemon.description,
    }
    if requested_pokemon.parent:
        previous_evolution = {
            'previous_evolution': {
                'title_ru': requested_pokemon.parent.title,
                'pokemon_id': requested_pokemon.parent.id,
                'img_url': requested_pokemon.parent.picture.url
            }
        }
        pokemon.update(previous_evolution)

    descendants = requested_pokemon.parent_to.all()
    if descendants:
        descendant = descendants[0]
        print(descendant)
        next_evolution = {
            'next_evolution': {
                'title_ru': descendant.title,
                'pokemon_id': descendant.id,
                'img_url': descendant.picture.url
            }
        }
        pokemon.update(next_evolution)

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
