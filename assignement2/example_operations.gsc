["abfolge",
["drucken",["multiplizieren",2,3]],
["drucken",["dividieren",9,3]],
["drucken",["potenzieren",2,3]],
["setzen", "bedingung", 0],
["drucken",["abrufen","bedingung"]],
["solange",["kleiner",["abrufen","bedingung"],10],
    ["abfolge",
        ["setzen","bedingung", ["addieren",["abrufen","bedingung"],1]],
        ["drucken",["abrufen","bedingung"]]
    ]
]
]