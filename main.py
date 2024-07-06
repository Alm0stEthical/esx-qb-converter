import os
import re
import customtkinter as ctk
from tkinter import messagebox, filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def load_conversion_patterns():
    patterns = [
        # Client-side patterns
        ("esx:onPlayerDeath", "hospital:server:SetDeathStatus"),
        ("esx:playerLoaded", "QBCore:Client:OnPlayerLoaded"),
        ("esx:showAdvancedNotification", "QBCore:Notify"),
        ("esx:showHelpNotification", "QBCore:Notify"),
        ("esx:showNotification", "QBCore:Notify"),
        ("ESX.GetPlayerData", "QBCore.Functions.GetPlayerData"),
        ("ESX.IsPlayerLoaded", "QBCore.Functions.GetPlayerData().citizenid ~= nil"),
        ("ESX.SetPlayerData", "QBCore:Player:SetPlayerData"),
        ("ESX.TriggerServerCallback", "QBCore.Functions.TriggerCallback"),
        ("ESX.Game.DeleteVehicle", "QBCore.Functions.DeleteVehicle"),
        ("ESX.Game.GetClosestPed", "QBCore.Functions.GetClosestPed"),
        ("ESX.Game.GetClosestPlayer", "QBCore.Functions.GetClosestPlayer"),
        ("ESX.Game.GetClosestVehicle", "QBCore.Functions.GetClosestVehicle"),
        ("ESX.Game.GetPlayers", "QBCore.Functions.GetPlayers"),
        ("ESX.Game.GetVehicles", "QBCore.Functions.GetVehicles"),
        ("ESX.Game.SetVehicleProperties", "QBCore.Functions.SetVehicleProperties"),
        ("ESX.Game.SpawnVehicle", "QBCore.Functions.SpawnVehicle"),
        ("ESX.Game.Utils.DrawText3D", "QBCore.Functions.DrawText3D"),
        # Server-side patterns
        ("ESX.GetPlayerFromId", "QBCore.Functions.GetPlayer"),
        ("ESX.GetPlayerFromIdentifier", "QBCore.Functions.GetPlayerByCitizenId"),
        ("ESX.GetPlayers", "QBCore.Functions.GetPlayers"),
        ("ESX.RegisterServerCallback", "QBCore.Functions.CreateCallback"),
        ("ESX.RegisterUsableItem", "QBCore.Functions.CreateUseableItem"),
        ("ESX.SavePlayer", "QBCore.Player.Save"),
        ("ESX.UseItem", "QBCore.Functions.UseItem"),
        ("xPlayer.removeWeaponComponent", "xPlayer.Functions.RemoveItem"),
        ("xPlayer.setAccountMoney", "xPlayer.Functions.SetMoney"),
        ("xPlayer.setInventoryItem", "xPlayer.Functions.AddItem"),
        ("xPlayer.setJob", "xPlayer.Functions.SetJob"),
        ("xPlayer.setMoney", "xPlayer.Functions.SetMoney"),
        ("xPlayer.showHelpNotification", "TriggerClientEvent('QBCore:Notify')"),
        ("xPlayer.showNotification", "TriggerClientEvent('QBCore:Notify')"),
        # Events
        ("esx:getSharedObject", "QBCore:GetObject"),
        ("esx:setJob", "QBCore:Client:OnJobUpdate"),
        ("esx:onPlayerSpawn", "QBCore:Client:OnPlayerLoaded"),
        ("playerSpawned", "QBCore:Client:OnPlayerLoaded"),
        ("esx:addInventoryItem", "QBCore:Server:AddItem"),
        ("esx:removeInventoryItem", "QBCore:Server:RemoveItem"),
        ("esx:useItem", "QBCore:Server:UseItem"),
        # Additional patterns
        ("ESX.Game.DeleteObject", "DeleteEntity"),
        ("ESX.Game.GetClosestObject", "GetClosestObjectOfType"),
        ("ESX.Game.GetPedMugshot", "RegisterPedheadshot"),
        ("ESX.Game.SpawnObject", "CreateObject"),
        ("ESX.Game.Teleport", "SetEntityCoords and SetEntityHeading"),
    ]
    return patterns + [(b, a) for a, b in patterns]


def manual_replace(script):
    script = script.replace(
        "local QBCore = exports['qb-core']:GetCoreObject()",
        "ESX = exports['es_extended']:getSharedObject()",
    )
    script = script.replace(
        "QBCore = exports['qb-core']:GetCoreObject()",
        "ESX = exports['es_extended']:getSharedObject()",
    )
    return script


def convert_script(script, patterns):
    script = manual_replace(script)
    for old, new in patterns:
        script = re.sub(old, new, script)
    return script


def process_file(file_path, patterns, direction):
    print(f"Processing file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    if direction == "ESX to QB-Core":
        converted = convert_script(
            content,
            [p for p in patterns if p[0].startswith("ESX") or p[0].startswith("esx")],
        )
    else:
        converted = convert_script(
            content,
            [p for p in patterns if p[0].startswith("QBCore") or p[0].startswith("QB")],
        )

    if content != converted:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(converted)
        print(f"Converted: {file_path}")
    else:
        print(f"No changes needed: {file_path}")


def process_folder(folder_path, patterns, direction, output_text):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".lua"):
                file_path = os.path.join(root, file)
                process_file(file_path, patterns, direction)
                output_text.insert(ctk.END, f"Processed: {file_path}\n")
                output_text.see(ctk.END)
                output_text.update_idletasks()


class ConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ESX/QB-Core Converter by dFuZe")
        self.geometry("600x400")
        self.patterns = load_conversion_patterns()
        self.create_widgets()

    def create_widgets(self):
        self.folder_path = ctk.StringVar()
        self.direction = ctk.StringVar(value="ESX to QB-Core")

        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(fill=ctk.X, padx=20, pady=(20, 10))
        ctk.CTkLabel(folder_frame, text="Select Folder:").pack(
            side=ctk.LEFT, padx=(0, 10)
        )
        ctk.CTkEntry(folder_frame, textvariable=self.folder_path).pack(
            side=ctk.LEFT, expand=True, fill=ctk.X
        )
        ctk.CTkButton(folder_frame, text="Browse", command=self.browse_folder).pack(
            side=ctk.LEFT, padx=(10, 0)
        )

        direction_frame = ctk.CTkFrame(self)
        direction_frame.pack(fill=ctk.X, padx=20, pady=10)
        ctk.CTkRadioButton(
            direction_frame,
            text="ESX to QB-Core",
            variable=self.direction,
            value="ESX to QB-Core",
        ).pack(side=ctk.LEFT)
        ctk.CTkRadioButton(
            direction_frame,
            text="QB-Core to ESX",
            variable=self.direction,
            value="QB-Core to ESX",
        ).pack(side=ctk.LEFT, padx=(20, 0))

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill=ctk.X, padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Convert", command=self.convert).pack(
            side=ctk.LEFT
        )
        ctk.CTkButton(button_frame, text="Exit", command=self.quit).pack(
            side=ctk.LEFT, padx=(20, 0)
        )

        self.output_text = ctk.CTkTextbox(self, wrap=ctk.WORD)
        self.output_text.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(0, 20))

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def convert(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder")
            return

        direction = self.direction.get()

        self.output_text.delete("1.0", ctk.END)
        self.output_text.insert(ctk.END, f"Starting conversion: {direction}\n")
        self.output_text.insert(ctk.END, f"Processing folder: {folder}\n")

        try:
            process_folder(folder, self.patterns, direction, self.output_text)
            self.output_text.insert(ctk.END, "\nConversion completed successfully!")
        except Exception as e:
            self.output_text.insert(ctk.END, f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()
