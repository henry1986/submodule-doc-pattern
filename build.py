#!/usr/bin/env python3
import json
import os

def build():
    # Load translations
    with open("translations.json", "r", encoding="utf-8") as f:
        translations = json.load(f)

    # Load template
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    languages = list(translations.keys())

    # Build hreflangs block
    hreflangs_lines = []
    for l in languages:
        filename = "index.html" if l == "de" else f"index_{l}.html"
        hreflangs_lines.append(f'<link rel="alternate" hreflang="{l}" href="{filename}" />')
    # Add x-default pointing to English or German (let's use English as x-default)
    hreflangs_lines.append('<link rel="alternate" hreflang="x-default" href="index_en.html" />')
    hreflangs_str = "\n    ".join(hreflangs_lines)

    # Simulator skeleton config (same across all languages)
    steps_skeleton = {
        "1": {
            "nodeClasses": {"lib": None, "docs": "active-node", "consumer": None},
            "arrows": {"1": False, "2": False},
            "arrowClasses": {}
        },
        "2": {
            "nodeClasses": {"lib": "active-node-secondary", "docs": "active-node", "consumer": None},
            "arrows": {"1": True, "2": False},
            "arrowClasses": {"1": "flow-active-secondary"}
        },
        "3": {
            "nodeClasses": {"lib": "active-node-secondary", "docs": "active-node", "consumer": None},
            "arrows": {"1": True, "2": False},
            "arrowClasses": {"1": "flow-active-secondary"}
        },
        "4": {
            "nodeClasses": {"lib": None, "docs": "active-node", "consumer": "active-node-secondary"},
            "arrows": {"1": False, "2": True},
            "arrowClasses": {"2": "flow-active"}
        },
        "5": {
            "nodeClasses": {"lib": None, "docs": "active-node-success", "consumer": "active-node-success"},
            "arrows": {"1": False, "2": True},
            "arrowClasses": {"2": "flow-active"}
        },
        "6": {
            "nodeClasses": {"lib": None, "docs": "active-node-success", "consumer": "active-node-success"},
            "arrows": {"1": False, "2": True},
            "arrowClasses": {"2": "flow-active"}
        }
    }

    for lang in languages:
        lang_trans = translations[lang]
        
        # Build stepsDataJS dynamically
        steps_data = {}
        for num in range(1, 7):
            num_str = str(num)
            steps_data[num_str] = {
                "title": lang_trans[f"sim_step_{num}_title"],
                "text": lang_trans[f"sim_step_{num}_exp"],
                "nodeClasses": steps_skeleton[num_str]["nodeClasses"],
                "arrows": steps_skeleton[num_str]["arrows"],
                "arrowClasses": steps_skeleton[num_str]["arrowClasses"]
            }

        steps_data_js = json.dumps(steps_data, ensure_ascii=False, indent=12)

        # Process page content
        output = template
        output = output.replace("{{lang}}", lang)
        
        # Map giscus lang codes properly
        giscus_lang = "zh-CN" if lang == "zh" else lang
        output = output.replace("{{giscus_lang}}", giscus_lang)
        
        output = output.replace("{{hreflangs}}", hreflangs_str)
        output = output.replace("{{stepsDataJS}}", steps_data_js)

        # Replace all translation keys
        for key, val in lang_trans.items():
            output = output.replace(f"{{{{{key}}}}}", val)

        # Write to target file
        output_filename = "index.html" if lang == "de" else f"index_{lang}.html"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(output)
        
        print(f"Generated {output_filename} ({lang})")

if __name__ == "__main__":
    build()
