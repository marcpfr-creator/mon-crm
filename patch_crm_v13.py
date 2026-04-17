#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║  Patch CRM Eastrategies v12 → v13 "Ma Journée"      ║
║  Usage: python3 patch_crm_v13.py                     ║
║         (placez ce fichier dans le même dossier       ║
║         que votre CRM HTML et le module)              ║
╚══════════════════════════════════════════════════════╝
"""
import sys, os

# Fichiers
MODULE_FILE = "eastrategies_journee_module.html"
INPUT_FILE  = input("Nom de votre fichier CRM actuel (ex: eastrategies.html): ").strip()
OUTPUT_FILE = INPUT_FILE.replace(".html", "_v13.html")

if not os.path.exists(INPUT_FILE):
    print(f"❌ Fichier introuvable: {INPUT_FILE}")
    sys.exit(1)

if not os.path.exists(MODULE_FILE):
    print(f"❌ Module introuvable: {MODULE_FILE}")
    print("   Téléchargez eastrategies_journee_module.html depuis Claude")
    sys.exit(1)

with open(MODULE_FILE, "r", encoding="utf-8") as f:
    module = f.read()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    html = f.read()

print(f"✓ CRM chargé: {len(html):,} chars")

modified = html
changes = 0

# Patch 1: Onglet "Ma Journée"
anchor1 = """switchTab('todo',this)">📝 Gestionnaire Tâches</button>"""
new1 = """switchTab('journee',this)">🗓 Ma Journée</button>\n  <button class="tab-btn" onclick="switchTab('todo',this)">📝 Gestionnaire Tâches</button>"""
if anchor1 in modified:
    modified = modified.replace(anchor1, new1, 1)
    print("✓ Patch 1: Onglet 'Ma Journée' ajouté")
    changes += 1
else:
    print("⚠ Patch 1: Ancre non trouvée (cherche l'onglet 'Gestionnaire Tâches')")

# Patch 2: switchTab routing
anchor2 = "if(name==='todo')       { tRender(); tSyncICloud(); }"
new2 = anchor2 + "\n  if(name==='journee')   { jRender(); jStartClock(); }"
if anchor2 in modified:
    modified = modified.replace(anchor2, new2, 1)
    print("✓ Patch 2: Routing switchTab étendu")
    changes += 1
else:
    print("⚠ Patch 2: Ancre switchTab non trouvée")

# Patch 3: Injection module avant </body>
if "</body>" in modified:
    modified = modified.replace("</body>", "\n" + module + "\n</body>", 1)
    print("✓ Patch 3: Module Ma Journée injecté")
    changes += 1
else:
    print("⚠ Patch 3: </body> non trouvé")

# Écrire le fichier patché
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(modified)

print(f"\n{'✅' if changes == 3 else '⚠'} Résultat: {changes}/3 patches appliqués")
print(f"📁 Fichier généré: {OUTPUT_FILE} ({len(modified):,} chars)")
if changes == 3:
    print("\n🎉 Mise à jour réussie ! Ouvrez " + OUTPUT_FILE + " dans votre navigateur.")
else:
    print("\n⚠ Certains patches ont échoué. Vérifiez que le fichier source est bien le CRM v12.")
