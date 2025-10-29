// Space Engineers drone script that supports renaming the subgrid and associated blocks.

using Sandbox.ModAPI.Ingame;
using SpaceEngineers.Game.ModAPI.Ingame;
using System;
using System.Collections.Generic;
using VRage.Game.ModAPI.Ingame;

namespace IngameScript
{
    partial class Program : MyGridProgram
    {
        public Program()
        {
        }

        public void Save()
        {
        }

        public void Main(string argument, UpdateType updateSource)
        {
            if (string.IsNullOrWhiteSpace(argument))
            {
                return;
            }

            string trimmed = argument.Trim();
            if (!trimmed.StartsWith("rename", StringComparison.OrdinalIgnoreCase))
            {
                return;
            }

            string newName = ExtractNameFromArgument(trimmed);
            if (string.IsNullOrWhiteSpace(newName))
            {
                Echo("Usage: rename <shipname>");
                return;
            }

            RenameSubgrid(newName);
        }

        private static string ExtractNameFromArgument(string argument)
        {
            string[] parts = argument.Split(new[] { ' ' }, 2, StringSplitOptions.RemoveEmptyEntries);
            if (parts.Length < 2)
            {
                return string.Empty;
            }

            return parts[1].Trim();
        }

        private void RenameSubgrid(string newName)
        {
            IMyCubeGrid grid = Me?.CubeGrid;
            if (grid == null)
            {
                Echo("Unable to locate the current subgrid.");
                return;
            }

            string oldName = grid.CustomName ?? string.Empty;

            var blocks = new List<IMyTerminalBlock>();
            GridTerminalSystem.GetBlocksOfType(blocks, block => block.CubeGrid == grid);

            foreach (IMyTerminalBlock block in blocks)
            {
                string suffix = ExtractSuffix(block.CustomName, oldName);
                string updatedName = ComposeName(newName, suffix);

                if (!string.Equals(block.CustomName, updatedName, StringComparison.Ordinal))
                {
                    block.CustomName = updatedName;
                }
            }

            if (!string.Equals(oldName, newName, StringComparison.Ordinal))
            {
                grid.CustomName = newName;
            }

            Echo($"Renamed subgrid '{oldName}' to '{newName}'.");
        }

        private static string ExtractSuffix(string customName, string prefix)
        {
            if (string.IsNullOrWhiteSpace(customName))
            {
                return string.Empty;
            }

            if (!string.IsNullOrWhiteSpace(prefix) && customName.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
            {
                string trimmed = customName.Substring(prefix.Length);
                return trimmed.TrimStart(' ', '-', '_', ':');
            }

            return customName;
        }

        private static string ComposeName(string prefix, string suffix)
        {
            if (string.IsNullOrWhiteSpace(prefix))
            {
                return suffix ?? string.Empty;
            }

            if (string.IsNullOrWhiteSpace(suffix))
            {
                return prefix.Trim();
            }

            return $"{prefix.Trim()} {suffix.Trim()}";
        }
    }
}
