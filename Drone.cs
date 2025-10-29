// Space Engineers drone automation script
// Automatically keeps block names aligned with the subgrid name,
// registers the drone with the central controller and refreshes
// the registration LCD panels.

// --- Begin Space Engineers boilerplate ---
using Sandbox.Game.EntityComponents;
using Sandbox.ModAPI.Ingame;
using Sandbox.ModAPI.Interfaces;
using SpaceEngineers.Game.ModAPI.Ingame;
using System;
using System.Collections.Generic;
using VRage.Game.GUI.TextPanel;
using VRage.Game.ModAPI.Ingame;
using VRage.Game.ModAPI.Ingame.Utilities;
using VRage.Game.ObjectBuilders.Definitions;
using VRageMath;

namespace IngameScript
{
    partial class Program : MyGridProgram
    {
        private readonly Drone _drone;

        public Program()
        {
            _drone = new Drone(this);
            Runtime.UpdateFrequency = UpdateFrequency.Update100;
        }

        public void Save()
        {
            _drone.SaveState();
        }

        public void Main(string argument, UpdateType updateSource)
        {
            _drone.Update(argument, updateSource);
        }

        private class Drone
        {
            private const string StorageSection = "Drone";
            private const string StorageNameKey = "SubgridName";
            private const string StorageSuffixSection = "Suffixes";
            private const string RegistrationBroadcastTag = "sven4-drone-registration";
            private const string RegistrationPanelTag = "registration place";
            private const int RegistrationIntervalTicks = 6; // Trigger roughly every 10 seconds on Update100

            private readonly Program _program;
            private readonly MyIni _ini = new MyIni();
            private readonly List<IMyTerminalBlock> _ownGridBlocks = new List<IMyTerminalBlock>();
            private readonly List<IMyTextPanel> _registrationPanels = new List<IMyTextPanel>();
            private readonly Dictionary<long, string> _suffixCache = new Dictionary<long, string>();

            private string _currentSubgridName;
            private int _registrationCountdown = 0;

            public Drone(Program program)
            {
                _program = program;
                _currentSubgridName = _program.Me?.CubeGrid?.CustomName ?? string.Empty;
                LoadState();
                RefreshOwnBlocks();
                UpdateRegistrationDisplays(forceRefresh: true);
            }

            public void Update(string argument, UpdateType updateSource)
            {
                string actualName = _program.Me?.CubeGrid?.CustomName ?? string.Empty;
                if (!string.Equals(actualName, _currentSubgridName, StringComparison.Ordinal))
                {
                    HandleGridRename(actualName);
                }

                if (_registrationCountdown <= 0)
                {
                    TryRegisterWithController(force: false);
                    _registrationCountdown = RegistrationIntervalTicks;
                }
                else
                {
                    _registrationCountdown--;
                }

                UpdateRegistrationDisplays();
            }

            public void SaveState()
            {
                _ini.Clear();
                _ini.Set(StorageSection, StorageNameKey, _currentSubgridName ?? string.Empty);
                _ini.DeleteSection(StorageSuffixSection);
                foreach (var pair in _suffixCache)
                {
                    _ini.Set(StorageSuffixSection, pair.Key.ToString(), pair.Value ?? string.Empty);
                }
                _program.Storage = _ini.ToString();
            }

            private void LoadState()
            {
                _suffixCache.Clear();
                _ini.Clear();
                if (!_ini.TryParse(_program.Storage))
                {
                    _ini.Clear();
                }

                string storedName = _ini.Get(StorageSection, StorageNameKey).ToString();
                if (!string.IsNullOrWhiteSpace(storedName))
                {
                    _currentSubgridName = storedName;
                }

                foreach (var key in _ini.GetKeys(StorageSuffixSection))
                {
                    long entityId;
                    if (long.TryParse(key.Name, out entityId))
                    {
                        string suffix = _ini.Get(StorageSuffixSection, key.Name).ToString();
                        if (!_suffixCache.ContainsKey(entityId))
                        {
                            _suffixCache.Add(entityId, suffix);
                        }
                    }
                }
            }

            private void HandleGridRename(string newName)
            {
                string oldName = _currentSubgridName;
                _currentSubgridName = newName ?? string.Empty;

                RefreshOwnBlocks();
                foreach (var block in _ownGridBlocks)
                {
                    string suffix = GetSuffixForBlock(block, oldName);
                    string newCustomName = ComposeName(_currentSubgridName, suffix);
                    if (!string.Equals(block.CustomName, newCustomName, StringComparison.Ordinal))
                    {
                        block.CustomName = newCustomName;
                    }
                }

                UpdateRegistrationDisplays(forceRefresh: true);
                TryRegisterWithController(force: true);
                SaveState();
            }

            private void RefreshOwnBlocks()
            {
                _ownGridBlocks.Clear();
                _program.GridTerminalSystem.GetBlocksOfType(_ownGridBlocks, block => block.CubeGrid == _program.Me?.CubeGrid);

                var validIds = new HashSet<long>();
                foreach (var block in _ownGridBlocks)
                {
                    validIds.Add(block.EntityId);
                    if (!_suffixCache.ContainsKey(block.EntityId))
                    {
                        _suffixCache[block.EntityId] = ExtractSuffix(block.CustomName, _currentSubgridName);
                    }
                }

                var stale = new List<long>();
                foreach (var pair in _suffixCache)
                {
                    if (!validIds.Contains(pair.Key))
                    {
                        stale.Add(pair.Key);
                    }
                }

                foreach (long id in stale)
                {
                    _suffixCache.Remove(id);
                }
            }

            private string GetSuffixForBlock(IMyTerminalBlock block, string previousPrefix)
            {
                if (block == null)
                {
                    return string.Empty;
                }

                string suffix;
                if (!_suffixCache.TryGetValue(block.EntityId, out suffix) || string.IsNullOrWhiteSpace(suffix))
                {
                    suffix = ExtractSuffix(block.CustomName, previousPrefix);
                    _suffixCache[block.EntityId] = suffix;
                }

                return suffix;
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

                return string.Format("{0} {1}", prefix.Trim(), suffix.Trim());
            }

            private void TryRegisterWithController(bool force)
            {
                if (_program?.IGC == null)
                {
                    return;
                }

                if (string.IsNullOrWhiteSpace(_currentSubgridName))
                {
                    _currentSubgridName = _program.Me?.CubeGrid?.CustomName ?? string.Empty;
                }

                string payload = string.Format("{0}|{1}", _currentSubgridName, _program.Me?.CubeGrid?.EntityId ?? 0);
                _program.IGC.SendBroadcastMessage(RegistrationBroadcastTag, payload);

                if (force)
                {
                    _registrationCountdown = RegistrationIntervalTicks;
                }
            }

            private void UpdateRegistrationDisplays(bool forceRefresh = false)
            {
                if (forceRefresh || _registrationPanels.Count == 0)
                {
                    _registrationPanels.Clear();
                    _program.GridTerminalSystem.GetBlocksOfType(_registrationPanels, panel =>
                        panel.CubeGrid == _program.Me?.CubeGrid &&
                        panel.CustomName.IndexOf(RegistrationPanelTag, StringComparison.OrdinalIgnoreCase) >= 0);
                }

                string text = _currentSubgridName ?? string.Empty;
                foreach (var panel in _registrationPanels)
                {
                    if (panel == null)
                    {
                        continue;
                    }

                    panel.ContentType = ContentType.TEXT_AND_IMAGE;
                    panel.WriteText(text);
                }
            }
        }
    }
}
