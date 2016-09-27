import redditbot as r

r.build_reply("[[Facebreaker]]")

assert r.build_reply("[Sire of Shards] is my favorite item") == None
assert r.build_reply("[Sire of Shards]] is my favorite item") == None
assert r.build_reply("[[]] is my favorite item") == None
assert r.build_reply("[[[Sire of Shards] is my favorite item") == None

#assert r.build_reply("[[]] [[Facebreaker]] [[Cast on crit]]") == None
#assert r.build_reply("[[Sire of Shards]] is my favorite item") == 'Sire of Shards'

item_panel, html = r.get_item_panel("Atziri's Splendour")
assert item_panel == "Atziri's Splendour (Armour, Evasion and Life)"
item_panel, html = r.get_item_panel("Vessel of Vinktar")
assert item_panel == "Vessel of Vinktar (Added Lightning Damage to Attacks)"
item_panel, html = r.get_item_panel("Facebreaker")
assert item_panel == "Facebreaker"
item_panel, html = r.get_item_panel("fvvvbasokeq")
assert item_panel == None and html == None
item_panel, html = r.get_item_panel("")
assert item_panel == None and html == None