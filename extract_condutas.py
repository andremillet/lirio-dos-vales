import os
import json

def extract_conducts():
    """
    Scans the current directory for .med files, extracts patient names from filenames,
    and parses the [CONDUTA] section from each file. The collected data is
    then saved into a single condutas.json file.
    """
    all_conducts = []
    files = [f for f in os.listdir('.') if f.lower().endswith('.med')]

    for filename in files:
        # Use the filename (without extension) as the patient's name
        patient_name = os.path.splitext(filename)[0]
        conducts = []
        in_conduct_section = False
        
        try:
            # Specify encoding to handle special characters
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    stripped_line = line.strip()
                    
                    # Start capturing when [CONDUTA] section is found
                    if stripped_line.lower() == '[conduta]':
                        in_conduct_section = True
                        continue
                    
                    # Stop capturing if a new section starts or not in the right section
                    if in_conduct_section:
                        if stripped_line.startswith('['):
                            break
                        # Add non-empty lines to the list
                        if stripped_line:
                            if stripped_line.startswith('++'):
                                conducts.append(f"DOSE AJUSTADA: {stripped_line[2:].strip()}")
                            elif stripped_line.startswith('+'):
                                conducts.append(f"ADICIONAR {stripped_line[1:].strip()} À LISTA DE MEDICAÇÕES")
                            else:
                                conducts.append(stripped_line)
            
            if conducts:
                all_conducts.append({
                    "paciente": patient_name,
                    "condutas": conducts
                })
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

    # Write the consolidated data to a JSON file
    with open('condutas.json', 'w', encoding='utf-8') as f:
        json.dump(all_conducts, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    extract_conducts()
    print("File 'condutas.json' created successfully with all patient conducts.")
