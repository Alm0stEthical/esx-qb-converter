import os
import re
import customtkinter as ctk
from tkinter import messagebox, filedialog


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def load_conversion_patterns():
    """
    Load conversion patterns for ESX to QB-Core and QB-Core to ESX.
    Patterns are organized alphabetically within their respective categories.

    Returns:
        dict: A dictionary containing lists of tuples for each conversion direction and SQL patterns.
    """
    patterns = {
        "ESX_to_QB_Core": [
            ("ESX.GetPlayerData", "QBCore.Functions.GetPlayerData"),
            ("ESX.IsPlayerLoaded", "QBCore.Functions.GetPlayerData().citizenid ~= nil"),
            ("ESX.SetPlayerData", "QBCore:Player:SetPlayerData"),
            ("ESX.TriggerServerCallback", "QBCore.Functions.TriggerCallback"),
            ("ESX.Game.DeleteVehicle", "QBCore.Functions.DeleteVehicle"),
            ("ESX.Game.DeleteObject", "DeleteEntity"),
            ("ESX.Game.GetClosestPed", "QBCore.Functions.GetClosestPed"),
            ("ESX.Game.GetClosestPlayer", "QBCore.Functions.GetClosestPlayer"),
            ("ESX.Game.GetClosestVehicle", "QBCore.Functions.GetClosestVehicle"),
            ("ESX.Game.GetClosestObject", "GetClosestObjectOfType"),
            ("ESX.Game.GetPedMugshot", "RegisterPedheadshot"),
            ("ESX.Game.GetPlayers", "QBCore.Functions.GetPlayers"),
            ("ESX.Game.GetVehicles", "QBCore.Functions.GetVehicles"),
            ("ESX.Game.GetVehicleProperties", "QBCore.Functions.GetVehicleProperties"),
            (
                "ESX.Game.GetVehicleInDirection",
                "QBCore.Functions.GetVehicleInDirection",
            ),
            ("ESX.Game.SpawnVehicle", "QBCore.Functions.SpawnVehicle"),
            ("ESX.Game.SpawnObject", "CreateObject"),
            (
                "ESX.Game.SetVehicleDoorsLocked",
                "QBCore.Functions.SetVehicleDoorsLocked",
            ),
            ("ESX.Game.SetVehicleProperties", "QBCore.Functions.SetVehicleProperties"),
            ("ESX.Game.Teleport", "SetEntityCoords and SetEntityHeading"),
            ("ESX.Game.Utils.DrawText3D", "QBCore.Functions.DrawText3D"),
            ("ESX.ShowInventory", "QBCore:Inventory"),
            ("ESX.ShowNotification", "QBCore:Notify"),
            ("ESX.ShowHelpNotification", "QBCore:Notify"),
            ("ESX.ShowAdvancedNotification", "QBCore:Notify"),
            ("ESX.SavePlayers", "QBCore.Functions.SavePlayers"),
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
            ("esx:addInventoryItem", "QBCore:Server:AddItem"),
            ("esx:getSharedObject", "QBCore:GetObject"),
            ("esx:onPlayerDeath", "hospital:server:SetDeathStatus"),
            ("esx:onPlayerSpawn", "QBCore:Client:OnPlayerLoaded"),
            ("esx:playerLoaded", "QBCore:Client:OnPlayerLoaded"),
            ("esx:removeInventoryItem", "QBCore:Server:RemoveItem"),
            ("esx:setAccountMoney", "QBCore:Server:SetMoney"),
            ("esx:showAdvancedNotification", "QBCore:Notify"),
            ("esx:showHelpNotification", "QBCore:Notify"),
            ("esx:showNotification", "QBCore:Notify"),
            ("esx:spawnVehicle", "QBCore:Command:SpawnVehicle"),
            ("esx:useItem", "QBCore:Server:UseItem"),
            ("playerSpawned", "QBCore:Client:OnPlayerLoaded"),
            ("exports.ghmattimysql.execute", "exports.oxmysql:execute"),
            ("exports.ghmattimysql.executeSync", "exports.oxmysql:executeSync"),
            ("exports.ghmattimysql.insert", "exports.oxmysql:insert"),
            ("exports.ghmattimysql.scalar", "exports.oxmysql:scalar"),
            ("exports.ghmattimysql.scalarSync", "exports.oxmysql:scalarSync"),
            ("MySQL.Async.execute", "exports.oxmysql:execute"),
            ("MySQL.Async.fetchAll", "exports.oxmysql:fetchAll"),
            ("MySQL.Async.fetchScalar", "exports.oxmysql:fetchScalar"),
            ("MySQL.Async.insert", "exports.oxmysql:insert"),
            ("MySQL.Sync.fetchAll", "exports.oxmysql:fetchAllSync"),
        ],
        "QB_Core_to_ESX": [
            ("QBCore.Functions.AddItem", "xPlayer.Functions.AddItem"),
            ("QBCore.Functions.CreateCallback", "ESX.RegisterServerCallback"),
            ("QBCore.Functions.CreateUseableItem", "ESX.RegisterUsableItem"),
            ("QBCore.Functions.DeleteVehicle", "ESX.Game.DeleteVehicle"),
            ("QBCore.Functions.DeleteEntity", "ESX.Game.DeleteObject"),
            ("QBCore.Functions.DrawText3D", "ESX.Game.Utils.DrawText3D"),
            ("QBCore.Functions.GetClosestPed", "ESX.Game.GetClosestPed"),
            ("QBCore.Functions.GetClosestPlayer", "ESX.Game.GetClosestPlayer"),
            ("QBCore.Functions.GetClosestVehicle", "ESX.Game.GetClosestVehicle"),
            ("QBCore.Functions.GetClosestObjectOfType", "ESX.Game.GetClosestObject"),
            ("QBCore.Functions.GetPedheadshot", "ESX.Game.GetPedMugshot"),
            ("QBCore.Functions.GetPlayer", "ESX.GetPlayerFromId"),
            ("QBCore.Functions.GetPlayerByCitizenId", "ESX.GetPlayerFromIdentifier"),
            ("QBCore.Functions.GetPlayerData", "ESX.GetPlayerData"),
            ("QBCore.Functions.GetPlayers", "ESX.GetPlayers"),
            (
                "QBCore.Functions.GetVehicleInDirection",
                "ESX.Game.GetVehicleInDirection",
            ),
            ("QBCore.Functions.GetVehicleProperties", "ESX.Game.GetVehicleProperties"),
            ("QBCore.Functions.Kick", "xPlayer.kick"),
            ("QBCore.Functions.Notify", "ESX.ShowNotification"),
            ("QBCore.Functions.OnJobUpdate", "esx:setJob"),
            ("QBCore.Functions.RemoveItem", "xPlayer.removeInventoryItem"),
            ("QBCore.Functions.RemoveMoney", "xPlayer.removeMoney"),
            ("QBCore.Functions.SavePlayers", "ESX.SavePlayers"),
            ("QBCore.Functions.SavePlayer", "ESX.SavePlayer"),
            ("QBCore.Functions.SetJob", "xPlayer.setJob"),
            ("QBCore.Functions.SetMoney", "xPlayer.setMoney"),
            ("QBCore.Functions.SetPlayerData", "ESX.SetPlayerData"),
            ("QBCore.Functions.SpawnVehicle", "ESX.Game.SpawnVehicle"),
            ("QBCore.Functions.TriggerCallback", "ESX.TriggerServerCallback"),
            ("QBCore.Functions.AddMoney", "xPlayer.addMoney"),
            ("QBCore.Functions.CreateCallback", "ESX.RegisterServerCallback"),
            ("QBCore.Functions.CreateUseableItem", "ESX.RegisterUsableItem"),
            ("QBCore.Functions.DeleteVehicle", "ESX.Game.DeleteVehicle"),
            ("QBCore.Functions.DeleteObject", "ESX.Game.DeleteObject"),
            ("QBCore.Functions.DrawText3D", "ESX.Game.Utils.DrawText3D"),
            ("QBCore.Functions.GetClosestPed", "ESX.Game.GetClosestPed"),
            ("QBCore.Functions.GetClosestPlayer", "ESX.Game.GetClosestPlayer"),
            ("QBCore.Functions.GetClosestVehicle", "ESX.Game.GetClosestVehicle"),
            ("QBCore.Functions.GetClosestObjectOfType", "ESX.Game.GetClosestObject"),
            ("QBCore.Functions.GetPedheadshot", "ESX.Game.GetPedMugshot"),
            ("QBCore.Functions.GetPlayerFromCoords", "ESX.GetPlayerFromCoords"),
            ("QBCore.Functions.GetPlayer", "ESX.GetPlayerFromId"),
            ("QBCore.Functions.GetPlayerByCitizenId", "ESX.GetPlayerFromIdentifier"),
            ("QBCore.Functions.GetPlayerData", "ESX.GetPlayerData"),
            ("QBCore.Functions.GetPlayers", "ESX.GetPlayers"),
            (
                "QBCore.Functions.GetVehicleInDirection",
                "ESX.Game.GetVehicleInDirection",
            ),
            ("QBCore.Functions.GetVehicleProperties", "ESX.Game.GetVehicleProperties"),
            ("QBCore.Functions.Kick", "xPlayer.kick"),
            ("QBCore.Functions.Notify", "ESX.ShowNotification"),
            ("QBCore.Functions.OnJobUpdate", "esx:setJob"),
            ("QBCore.Functions.RemoveItem", "xPlayer.removeInventoryItem"),
            ("QBCore.Functions.RemoveMoney", "xPlayer.removeMoney"),
            ("QBCore.Functions.SavePlayers", "ESX.SavePlayers"),
            ("QBCore.Functions.SavePlayer", "ESX.SavePlayer"),
            ("QBCore.Functions.SetJob", "xPlayer.setJob"),
            ("QBCore.Functions.SetMoney", "xPlayer.setMoney"),
            ("QBCore.Functions.SetPlayerData", "ESX.SetPlayerData"),
            ("QBCore.Functions.SpawnVehicle", "ESX.Game.SpawnVehicle"),
            ("QBCore.Functions.TriggerCallback", "ESX.TriggerServerCallback"),
            ("QBCore:GetObject", "esx:getSharedObject"),
            ("QBCore:Server:AddItem", "esx:addInventoryItem"),
            ("QBCore:Server:RemoveItem", "esx:removeInventoryItem"),
            ("QBCore:Server:SetMoney", "esx:setAccountMoney"),
            ("QBCore:Server:UseItem", "esx:useItem"),
            ("QBCore:Client:OnJobUpdate", "esx:setJob"),
            ("QBCore:Client:OnPlayerLoaded", "esx:onPlayerLoaded"),
            ("QBCore:Client:OnPlayerDeath", "esx:onPlayerDeath"),
            ("QBCore:Client:OnPlayerSpawn", "esx:onPlayerSpawn"),
            ("exports.oxmysql:execute", "exports.ghmattimysql.execute"),
            ("exports.oxmysql:executeSync", "exports.ghmattimysql.executeSync"),
            ("exports.oxmysql:insert", "exports.ghmattimysql.insert"),
            ("exports.oxmysql:scalar", "exports.ghmattimysql.scalar"),
            ("exports.oxmysql:scalarSync", "exports.ghmattimysql.scalarSync"),
            ("exports.oxmysql:fetchAll", "exports.ghmattimysql.execute"),
            ("exports.oxmysql:fetchScalar", "exports.ghmattimysql.execute"),
            ("exports.oxmysql:fetch", "ghmattimysql:execute"),
        ],
        "SQL_patterns": [
            ("exports.ghmattimysql.execute('UPDATE ", "oxmysql:execute('UPDATE "),
            ("exports.ghmattimysql.execute('DELETE ", "oxmysql:execute('DELETE "),
            ("exports.ghmattimysql.execute('SELECT ", "oxmysql:fetch('SELECT "),
            ("['ghmattimysql']:execute('UPDATE ", ".oxmysql:execute('UPDATE "),
            ("['ghmattimysql']:execute('DELETE ", ".oxmysql:execute('DELETE "),
            ("['ghmattimysql']:execute('SELECT ", ".oxmysql:fetch('SELECT "),
            ("['ghmattimysql']:execute('INSERT ", ".oxmysql:insert('INSERT "),
            ("exports.ghmattimysql.execute", "exports.oxmysql:execute"),
            ("exports.ghmattimysql.executeSync", "exports.oxmysql:executeSync"),
            ("exports.ghmattimysql.scalar", "exports.oxmysql:scalar"),
            ("exports.ghmattimysql.scalarSync", "exports.oxmysql:scalarSync"),
            ("MySQL.Async.execute", "exports.oxmysql:execute"),
            ("MySQL.Async.fetchAll", "exports.oxmysql:fetchAll"),
            ("MySQL.Async.fetchScalar", "exports.oxmysql:fetchScalar"),
            ("MySQL.Async.insert", "exports.oxmysql:insert"),
            ("MySQL.Sync.fetchAll", "exports.oxmysql:fetchAllSync"),
        ],
    }
    return patterns


def manual_replace(script):
    """
    Perform manual replacements that are not covered by the regex patterns.

    Args:
        script (str): The content of the script file.

    Returns:
        str: The modified script content.
    """
    replacements = {
        "local QBCore = exports['qb-core']:GetCoreObject()": "ESX = exports['es_extended']:getSharedObject()",
        "QBCore = exports['qb-core']:GetCoreObject()": "ESX = exports['es_extended']:getSharedObject()",
    }

    for old, new in replacements.items():
        script = script.replace(old, new)

    return script


def convert_script(script, patterns, include_sql=False, sql_patterns=[]):
    """
    Convert the script content based on the provided patterns.

    Args:
        script (str): The original script content.
        patterns (list): List of tuples containing old and new patterns.
        include_sql (bool): Flag to include SQL patterns.
        sql_patterns (list): List of SQL pattern tuples.

    Returns:
        str: The converted script content.
    """
    script = manual_replace(script)
    for old, new in patterns:
        script = re.sub(re.escape(old), new, script)
    if include_sql:
        for old, new in sql_patterns:
            script = re.sub(re.escape(old), new, script)
    return script


def process_file(file_path, patterns, direction, include_sql, sql_patterns):
    """
    Process a single Lua script file, converting its content based on the patterns.

    Args:
        file_path (str): Path to the Lua script file.
        patterns (list): List of tuples containing old and new patterns.
        direction (str): Conversion direction ("ESX to QB-Core" or "QB-Core to ESX").
        include_sql (bool): Flag to include SQL patterns.
        sql_patterns (list): List of SQL pattern tuples.
    """
    print(f"Processing file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    converted = convert_script(content, patterns, include_sql, sql_patterns)

    if content != converted:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(converted)
        print(f"Converted: {file_path}")
    else:
        print(f"No changes needed: {file_path}")


def process_folder(
    folder_path, patterns, direction, include_sql, sql_patterns, output_text
):
    """
    Recursively process all Lua script files in the specified folder.

    Args:
        folder_path (str): Path to the folder containing Lua script files.
        patterns (list): List of tuples containing old and new patterns.
        direction (str): Conversion direction ("ESX to QB-Core" or "QB-Core to ESX").
        include_sql (bool): Flag to include SQL patterns.
        sql_patterns (list): List of SQL pattern tuples.
        output_text (ctk.CTkTextbox): Textbox widget to display output logs.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".lua"):
                file_path = os.path.join(root, file)
                process_file(file_path, patterns, direction, include_sql, sql_patterns)
                output_text.insert(ctk.END, f"Processed: {file_path}\n")
                output_text.see(ctk.END)
                output_text.update_idletasks()


class ConverterApp(ctk.CTk):
    """
    The main application class for the ESX/QB-Core Converter.
    """

    def __init__(self):
        super().__init__()
        self.title("ESX/QB-Core Converter by dFuZe & densuz")
        self.geometry("700x600")
        self.patterns = load_conversion_patterns()
        self.create_widgets()

    def create_widgets(self):
        """
        Create and layout all GUI widgets.
        """

        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(fill=ctk.X, padx=20, pady=(20, 10))

        ctk.CTkLabel(folder_frame, text="Select Folder:").pack(
            side=ctk.LEFT, padx=(0, 10)
        )

        self.folder_path = ctk.StringVar()
        ctk.CTkEntry(folder_frame, textvariable=self.folder_path).pack(
            side=ctk.LEFT, expand=True, fill=ctk.X
        )

        ctk.CTkButton(folder_frame, text="Browse", command=self.browse_folder).pack(
            side=ctk.LEFT, padx=(10, 0)
        )

        direction_frame = ctk.CTkFrame(self)
        direction_frame.pack(fill=ctk.X, padx=20, pady=10)

        self.direction = ctk.StringVar(value="ESX to QB-Core")
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

        sql_frame = ctk.CTkFrame(self)
        sql_frame.pack(fill=ctk.X, padx=20, pady=10)

        self.include_sql = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            sql_frame,
            text="Include SQL Patterns",
            variable=self.include_sql,
        ).pack(side=ctk.LEFT)

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
        """
        Open a dialog to select a folder and set the folder path.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def convert(self):
        """
        Start the conversion process based on user input.
        """
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder")
            return

        direction = self.direction.get()
        include_sql = self.include_sql.get()

        self.output_text.delete("1.0", ctk.END)
        self.output_text.insert(ctk.END, f"Starting conversion: {direction}\n")
        self.output_text.insert(ctk.END, f"Processing folder: {folder}\n")
        self.output_text.insert(
            ctk.END, f"Include SQL Patterns: {'Yes' if include_sql else 'No'}\n\n"
        )

        if direction == "ESX to QB-Core":
            selected_patterns = self.patterns["ESX_to_QB_Core"]
        else:
            selected_patterns = self.patterns["QB_Core_to_ESX"]

        sql_patterns = self.patterns.get("SQL_patterns", [])

        try:
            process_folder(
                folder,
                selected_patterns,
                direction,
                include_sql,
                sql_patterns,
                self.output_text,
            )
            self.output_text.insert(ctk.END, "\nConversion completed successfully!")
        except Exception as e:
            self.output_text.insert(ctk.END, f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()
