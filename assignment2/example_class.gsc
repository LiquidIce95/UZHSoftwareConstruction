[
  "abfolge",
    ["setzen", "Shape", 
      ["klasse",["name"], 
        [["setzen", "shape_density", ["funktion", ["weight", "volume"], ["dividieren", ["abrufen", "weight"], ["abrufen", "volume"]]]]
        ]
      ]
    ],
    ["setzen", "Circle", 
      ["klasse","Shape",["radius"], 
        [["setzen", "circle_area", ["funktion", ["radius"], ["multiplizieren", 3.1415926535897932385, ["potenzieren", ["abrufen", "radius"], 2]]]]
        ]
      ]
    ],
    ["setzen", "Square", 
      ["klasse","Shape",["side"], 
        [["setzen", "square_area", ["funktion", ["side"], ["multiplizieren", ["abrufen", "side"], ["abrufen", "side"]]]]
        ]
      ]
    ],
    ["setzen", "mySquare", ["machen", "Square", ["sq", 3]]],
    ["setzen", "myCircle", ["machen", "Circle", ["ci", 2]]],
    ["setzen", "weight", 5],
    ["setzen", "volume_square", ["ausführen", ["mySquare", "square_area"]]],
    ["setzen", "volume_circle", ["ausführen", ["myCircle", "circle_area"]]],
    ["addieren", ["ausführen", ["mySquare", "shape_density", ["abrufen", "weight"], ["abrufen", "volume_square"]]], ["ausführen", ["myCircle", "shape_density", ["abrufen", "weight"], ["abrufen", "volume_circle"]]]]
]
