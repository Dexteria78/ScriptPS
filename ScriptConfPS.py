#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Générateur de configuration réseau avec interface graphique moderne
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

class NetworkConfigGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Config Generator")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Couleurs modernes
        self.colors = {
            'bg': '#0f172a',
            'secondary_bg': '#1e293b',
            'card_bg': '#334155',
            'accent': '#3b82f6',
            'accent_hover': '#2563eb',
            'success': '#10b981',
            'text': '#f1f5f9',
            'text_secondary': '#94a3b8',
            'border': '#475569'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Liste pour stocker les widgets de chaque subnet
        self.subnet_widgets = []
        self.num_subnets = 1
        
        self.create_widgets()
    
    def create_widgets(self):
        # Canvas principal avec scrollbar
        self.canvas = tk.Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame principal avec padding
        main_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg'], padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # En-tête avec icône
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        title = tk.Label(header_frame,
                         text="Network Configuration Generator",
                         font=('Segoe UI', 24, 'bold'),
                         fg=self.colors['text'],
                         bg=self.colors['bg'])
        title.pack()

        subtitle = tk.Label(header_frame,
                            text="Generate ISI network commands with ease",
                            font=('Segoe UI', 11),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['bg'])
        subtitle.pack(pady=(5, 0))
        
        # Card pour le groupnet
        groupnet_card = tk.Frame(main_frame, bg=self.colors['secondary_bg'], 
                            relief=tk.FLAT, bd=0)
        groupnet_card.pack(fill=tk.X, pady=(0, 20))
        
        groupnet_inner = tk.Frame(groupnet_card, bg=self.colors['secondary_bg'], padx=30, pady=30)
        groupnet_inner.pack(fill=tk.BOTH, expand=True)
        
        # Groupnet
        groupnet_label = tk.Label(groupnet_inner,
                           text="Groupnet Name",
                           font=('Segoe UI', 11, 'bold'),
                           fg=self.colors['text'],
                           bg=self.colors['secondary_bg'])
        groupnet_label.pack(anchor=tk.W)
        
        opt_label = tk.Label(groupnet_inner,
                           text="Optional",
                           font=('Segoe UI', 9),
                           fg=self.colors['text_secondary'],
                           bg=self.colors['secondary_bg'])
        opt_label.pack(anchor=tk.W)
        
        self.groupnet_var = tk.StringVar()
        entry = tk.Entry(groupnet_inner, textvariable=self.groupnet_var,
                        font=('Segoe UI', 11),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text'],
                        insertbackground=self.colors['text'],
                        relief=tk.FLAT,
                        bd=0,
                        highlightthickness=2,
                        highlightcolor=self.colors['accent'],
                        highlightbackground=self.colors['border'])
        entry.pack(fill=tk.X, pady=(8, 0), ipady=8, ipadx=12)
        
        # Nombre de subnets
        subnet_count_card = tk.Frame(main_frame, bg=self.colors['secondary_bg'], 
                            relief=tk.FLAT, bd=0)
        subnet_count_card.pack(fill=tk.X, pady=(0, 20))
        
        subnet_count_inner = tk.Frame(subnet_count_card, bg=self.colors['secondary_bg'], padx=30, pady=30)
        subnet_count_inner.pack(fill=tk.BOTH, expand=True)
        
        count_label = tk.Label(subnet_count_inner,
                               text="Number of Subnets",
                               font=('Segoe UI', 13, 'bold'),
                               fg=self.colors['text'],
                               bg=self.colors['secondary_bg'])
        count_label.pack(anchor=tk.W, pady=(0, 15))
        
        count_frame = tk.Frame(subnet_count_inner, bg=self.colors['secondary_bg'])
        count_frame.pack(fill=tk.X)
        
        self.subnet_count_var = tk.IntVar(value=1)
        tk.Spinbox(count_frame,
                  from_=1,
                  to=10,
                  textvariable=self.subnet_count_var,
                  font=('Segoe UI', 11),
                  bg=self.colors['card_bg'],
                  fg=self.colors['text'],
                  buttonbackground=self.colors['accent'],
                  relief=tk.FLAT,
                  bd=0,
                  width=10,
                  command=self.update_subnet_fields).pack(side=tk.LEFT)
        
        tk.Button(count_frame,
                 text="Apply",
                 command=self.update_subnet_fields,
                 font=('Segoe UI', 10, 'bold'),
                 fg=self.colors['text'],
                 bg=self.colors['accent'],
                 activebackground=self.colors['accent_hover'],
                 activeforeground=self.colors['text'],
                 relief=tk.FLAT,
                 bd=0,
                 cursor='hand2',
                 padx=20,
                 pady=8).pack(side=tk.LEFT, padx=(10, 0))
        
        # Container pour les subnets
        self.subnets_container = tk.Frame(main_frame, bg=self.colors['bg'])
        self.subnets_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Créer le premier subnet
        self.create_subnet_fields()
        
        # Boutons d'action
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        def create_button(parent, text, command, primary=False):
            btn_bg = self.colors['accent'] if primary else self.colors['card_bg']
            btn = tk.Button(parent,
                          text=text,
                          command=command,
                          font=('Segoe UI', 11, 'bold'),
                          fg=self.colors['text'],
                          bg=btn_bg,
                          activebackground=self.colors['accent_hover'] if primary else self.colors['border'],
                          activeforeground=self.colors['text'],
                          relief=tk.FLAT,
                          bd=0,
                          cursor='hand2',
                          padx=25,
                          pady=12)
            
            # Effet hover
            def on_enter(e):
                btn['background'] = self.colors['accent_hover'] if primary else self.colors['border']
            def on_leave(e):
                btn['background'] = btn_bg
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
            
            return btn
        
        create_button(btn_frame, "Generate Preview", self.generate_preview, primary=True).pack(side=tk.LEFT, padx=(0, 10))
        create_button(btn_frame, "Save to File", self.save_file).pack(side=tk.LEFT, padx=(0, 10))
        create_button(btn_frame, "Reset", self.reset_form).pack(side=tk.LEFT)
        
        # Card pour l'aperçu
        preview_card = tk.Frame(main_frame, bg=self.colors['secondary_bg'], relief=tk.FLAT, bd=0)
        preview_card.pack(fill=tk.BOTH, expand=True)
        
        preview_inner = tk.Frame(preview_card, bg=self.colors['secondary_bg'], padx=30, pady=30)
        preview_inner.pack(fill=tk.BOTH, expand=True)
        
        preview_label = tk.Label(preview_inner,
                                 text="Command Preview",
                                 font=('Segoe UI', 13, 'bold'),
                                 fg=self.colors['text'],
                                 bg=self.colors['secondary_bg'])
        preview_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Text widget pour l'aperçu avec style terminal
        self.preview_text = tk.Text(preview_inner,
                                   height=12,
                                   wrap=tk.WORD,
                                   font=('Cascadia Code', 10),
                                   bg='#0d1117',
                                   fg='#58a6ff',
                                   insertbackground='#58a6ff',
                                   relief=tk.FLAT,
                                   bd=0,
                                   padx=15,
                                   pady=15,
                                   selectbackground='#1f6feb',
                                   selectforeground='#ffffff')
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Pack canvas et scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mouse wheel pour Linux et Windows
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_mousewheel_linux(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        
        # Windows/MacOS
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux
        self.canvas.bind_all("<Button-4>", _on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", _on_mousewheel_linux)
    
    def create_subnet_fields(self):
        """Crée les champs pour un subnet"""
        subnet_num = len(self.subnet_widgets) + 1
        
        # Card pour le subnet
        subnet_card = tk.Frame(self.subnets_container, bg=self.colors['secondary_bg'], 
                              relief=tk.FLAT, bd=0)
        subnet_card.pack(fill=tk.X, pady=(0, 15))
        
        subnet_inner = tk.Frame(subnet_card, bg=self.colors['secondary_bg'], padx=30, pady=30)
        subnet_inner.pack(fill=tk.BOTH, expand=True)
        
        # Titre du subnet
        subnet_title = tk.Label(subnet_inner,
                               text=f"Subnet #{subnet_num}",
                               font=('Segoe UI', 13, 'bold'),
                               fg=self.colors['text'],
                               bg=self.colors['secondary_bg'])
        subnet_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Dictionnaire pour stocker les variables
        subnet_vars = {}
        
        # Fonction pour créer un champ
        def create_field(parent, label_text, var_name, optional=False):
            field_frame = tk.Frame(parent, bg=self.colors['secondary_bg'])
            field_frame.pack(fill=tk.X, pady=8)
            
            label = tk.Label(field_frame,
                           text=label_text,
                           font=('Segoe UI', 10, 'bold'),
                           fg=self.colors['text'],
                           bg=self.colors['secondary_bg'])
            label.pack(anchor=tk.W)
            
            if optional:
                opt_label = tk.Label(field_frame,
                                   text="Optional",
                                   font=('Segoe UI', 8),
                                   fg=self.colors['text_secondary'],
                                   bg=self.colors['secondary_bg'])
                opt_label.pack(anchor=tk.W)
            
            var = tk.StringVar()
            subnet_vars[var_name] = var
            
            entry = tk.Entry(field_frame, textvariable=var,
                            font=('Segoe UI', 10),
                            bg=self.colors['card_bg'],
                            fg=self.colors['text'],
                            insertbackground=self.colors['text'],
                            relief=tk.FLAT,
                            bd=0,
                            highlightthickness=2,
                            highlightcolor=self.colors['accent'],
                            highlightbackground=self.colors['border'])
            entry.pack(fill=tk.X, pady=(5, 0), ipady=6, ipadx=10)
        
        # Créer les champs
        create_field(subnet_inner, "Subnet Name", "subnet")
        create_field(subnet_inner, "Gateway", "gateway")
        
        # Mode Address (Radio buttons)
        field_frame = tk.Frame(subnet_inner, bg=self.colors['secondary_bg'])
        field_frame.pack(fill=tk.X, pady=8)
        
        label = tk.Label(field_frame,
                       text="Address Family",
                       font=('Segoe UI', 10, 'bold'),
                       fg=self.colors['text'],
                       bg=self.colors['secondary_bg'])
        label.pack(anchor=tk.W)
        
        addr_var = tk.StringVar(value="ipv4")
        subnet_vars["addr_family"] = addr_var
        
        radio_frame = tk.Frame(field_frame, bg=self.colors['secondary_bg'])
        radio_frame.pack(fill=tk.X, pady=(5, 0))
        
        for value, text in [("ipv4", "IPv4"), ("ipv6", "IPv6")]:
            rb = tk.Radiobutton(radio_frame,
                               text=text,
                               variable=addr_var,
                               value=value,
                               font=('Segoe UI', 9),
                               fg=self.colors['text'],
                               bg=self.colors['secondary_bg'],
                               selectcolor=self.colors['accent'],
                               activebackground=self.colors['secondary_bg'],
                               activeforeground=self.colors['text'],
                               bd=0,
                               highlightthickness=0)
            rb.pack(side=tk.LEFT, padx=(0, 15))
        
        create_field(subnet_inner, "Prefix Length", "prefixlen")
        create_field(subnet_inner, "VLAN ID", "vlan_id", optional=True)
        create_field(subnet_inner, "SSIP Address", "ssip")
        
        # Stocker les widgets et variables
        self.subnet_widgets.append({
            'card': subnet_card,
            'vars': subnet_vars
        })
    
    def update_subnet_fields(self):
        """Met à jour le nombre de champs subnet"""
        new_count = self.subnet_count_var.get()
        current_count = len(self.subnet_widgets)
        
        if new_count > current_count:
            # Ajouter des subnets
            for _ in range(new_count - current_count):
                self.create_subnet_fields()
        elif new_count < current_count:
            # Supprimer des subnets
            for _ in range(current_count - new_count):
                widget = self.subnet_widgets.pop()
                widget['card'].destroy()
        
        # Mettre à jour la région de scroll
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def generate_commands(self):
        """Génère les commandes selon les valeurs du formulaire"""
        commands = []
        
        groupnet = self.groupnet_var.get().strip()
        
        # Commande groupnet
        if groupnet:
            commands.append(f"isi network groupnets modify groupnet0 --name={groupnet}")
        
        # Commandes pour chaque subnet
        for i, subnet_widget in enumerate(self.subnet_widgets, 1):
            vars = subnet_widget['vars']
            
            subnet = vars['subnet'].get().strip()
            gateway = vars['gateway'].get().strip()
            addr_family = vars['addr_family'].get()
            prefixlen = vars['prefixlen'].get().strip()
            vlan_id = vars['vlan_id'].get().strip()
            ssip = vars['ssip'].get().strip()
            
            # Commande subnet
            if subnet:
                groupnet_name = groupnet if groupnet else "groupnet0"
                cmd = f"isi network subnet create {groupnet_name}.{subnet}"
                
                if addr_family:
                    cmd += f" --addr-family={addr_family}"
                
                if gateway:
                    cmd += f" --gateway={gateway}"
                
                if prefixlen:
                    cmd += f" --prefixlen={prefixlen}"
                
                if vlan_id:
                    cmd += f" --vlan-id={vlan_id} --vlan-enable=true"
                
                if ssip:
                    cmd += f" --sc-service-addrs={ssip}"
                
                commands.append(cmd)
        
        return commands
    
    def generate_preview(self):
        """Affiche l'aperçu des commandes"""
        commands = self.generate_commands()
        
        self.preview_text.delete(1.0, tk.END)
        
        if commands:
            # Insère seulement les commandes, sans en-tête supplémentaire
            for cmd in commands:
                self.preview_text.insert(tk.END, f"{cmd}\n\n")
        else:
            # Message en français quand aucune commande n'est générée
            self.preview_text.insert(tk.END, "# Aucune commande générée\n# Veuillez remplir au moins un champ Subnet")
    
    def save_file(self):
        """Sauvegarde les commandes dans un fichier"""
        commands = self.generate_commands()
        
        if not commands:
            messagebox.showwarning("Warning", 
                                  "No commands to save.\nPlease fill in at least one Subnet field.",
                                  parent=self.root)
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="network_config.txt",
            parent=self.root
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for cmd in commands:
                        f.write(cmd + '\n')
                messagebox.showinfo("Success", 
                                   f"File '{Path(filename).name}' created successfully!",
                                   parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", 
                                    f"Error while saving:\n{str(e)}",
                                    parent=self.root)
    
    def reset_form(self):
        """Réinitialise le formulaire"""
        self.groupnet_var.set("")
        
        for subnet_widget in self.subnet_widgets:
            for var in subnet_widget['vars'].values():
                if isinstance(var, tk.StringVar):
                    if var == subnet_widget['vars'].get('addr_family'):
                        var.set("ipv4")
                    else:
                        var.set("")
        
        self.preview_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = NetworkConfigGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
