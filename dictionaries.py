from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
images_folder = os.path.join(BASE_DIR, "images")

commanders ={

    "Charles Martel":{
        "search": [
            "Martel",
            "Charles",
            "Charles Martel"
        ],
        "rarity": "Legendary",
        "skills": [
            "Infantry",
            "Garrison",
            "Defence"
        ],
        "title": "The Immortal Hammer",
        "type": "Infantry",

        "roles": {
            "city defense": {
                "attack": 6,
                "defence": 5,
                "health": 4,
                "march speed": 0,
                "build": os.path.join(images_folder, "charles-martel-city-garrison.jpeg"),
                "pairings": [
                    "Constanine I (Secondary)",
                    "Wu Zetian (Primary)",
                    "Yi Seong-Gye (Secondary)",
                    "Eulji Mundeok (Seconadary)",
                    "Sun Tzu (Secondary)"
                ],
            },
            "flag defence": {
                "attack": 6,
                "defence": 5,
                "health": 4,
                "march speed": 0,
                "build": os.path.join(images_folder, "charles-martel-flag-garrison.jpeg"),
                "pairings": [
                    "Constanine I (Secondary)",
                    "Wu Zetian (Primary)",
                    "Yi Seong-Gye (Secondary)",
                    "Eulji Mundeok (Seconadary)",
                    "Sun Tzu (Secondary)"
                ],
            },
            "open field": {
                "attack": 10,
                "defence": 9.5,
                "health": 13,
                "march speed": 24,
                "build": os.path.join(images_folder, "charles-martel-open-field.jpeg"),
                "pairings": [
                    "Alexander The Great (Primary)",
                    "Richard I (Primary)",
                    "Yi Seong-Gye (Secondary)",
                    "Eulji Mundeok (Secondary)",
                    "Sun Tzu (Secondary)"
                ],
            },
            
            
        }
    }

}