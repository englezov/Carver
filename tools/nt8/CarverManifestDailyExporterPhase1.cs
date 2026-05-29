// Phase-1 manifest-driven NinjaTrader Desktop daily export helper for Carver.
// Import into NinjaTrader 8 only after a separate operator execution gate.
// Defaults to disarmed. When explicitly armed, it requests only the hard-coded
// MES/ZN/ZF source-native daily Last rows listed in the phase-1 manifest and
// writes NinjaTrader-native semicolon text files to the Carver quarantine.

#region Using declarations
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.IO;
using NinjaTrader.Cbi;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.Indicators;
#endregion

namespace NinjaTrader.NinjaScript.Indicators
{
    public class CarverManifestDailyExporterPhase1 : Indicator
    {
        private const string LockedManifestId = "CARVER_PARTS_1_3_DAILY_SEED_MULTI_ASSET_PHASE1_MES_ZN_ZF";
        private const string LockedOutputRoot = @"C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\native_daily_exports";
        private readonly List<BarsRequest> activeRequests = new List<BarsRequest>();
        private bool started;
        private int pendingRequests;

        private sealed class ExportRow
        {
            public string Root { get; private set; }
            public string ContractMonth { get; private set; }
            public string NinjaTraderSymbol { get; private set; }
            public string StartDate { get; private set; }
            public string EndDate { get; private set; }
            public string NativeFile { get; private set; }

            public ExportRow(string root, string contractMonth, string ninjaTraderSymbol, string startDate, string endDate, string nativeFile)
            {
                Root = root;
                ContractMonth = contractMonth;
                NinjaTraderSymbol = ninjaTraderSymbol;
                StartDate = startDate;
                EndDate = endDate;
                NativeFile = nativeFile;
            }
        }

        private static readonly ExportRow[] ManifestRows = new[]
        {
            new ExportRow("MES", "09-25", "MES SEP25", "2025-05-29", "2026-05-28", @"MES\MES 09-25.Last.txt"),
            new ExportRow("MES", "12-25", "MES DEC25", "2025-05-29", "2026-05-28", @"MES\MES 12-25.Last.txt"),
            new ExportRow("MES", "03-26", "MES MAR26", "2025-05-29", "2026-05-28", @"MES\MES 03-26.Last.txt"),
            new ExportRow("MES", "06-26", "MES JUN26", "2025-05-29", "2026-05-28", @"MES\MES 06-26.Last.txt"),
            new ExportRow("ZN", "09-25", "ZN SEP25", "2025-05-29", "2026-05-28", @"ZN\ZN 09-25.Last.txt"),
            new ExportRow("ZN", "12-25", "ZN DEC25", "2025-05-29", "2026-05-28", @"ZN\ZN 12-25.Last.txt"),
            new ExportRow("ZN", "03-26", "ZN MAR26", "2025-05-29", "2026-05-28", @"ZN\ZN 03-26.Last.txt"),
            new ExportRow("ZN", "06-26", "ZN JUN26", "2025-05-29", "2026-05-28", @"ZN\ZN 06-26.Last.txt"),
            new ExportRow("ZF", "09-25", "ZF SEP25", "2025-05-29", "2026-05-28", @"ZF\ZF 09-25.Last.txt"),
            new ExportRow("ZF", "12-25", "ZF DEC25", "2025-05-29", "2026-05-28", @"ZF\ZF 12-25.Last.txt"),
            new ExportRow("ZF", "03-26", "ZF MAR26", "2025-05-29", "2026-05-28", @"ZF\ZF 03-26.Last.txt"),
            new ExportRow("ZF", "06-26", "ZF JUN26", "2025-05-29", "2026-05-28", @"ZF\ZF 06-26.Last.txt"),
        };

        [NinjaScriptProperty]
        [Display(Name = "Execution armed", Order = 1, GroupName = "Carver")]
        public bool ExecutionArmed { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Expected manifest id", Order = 2, GroupName = "Carver")]
        public string ExpectedManifestId { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Output root", Order = 3, GroupName = "Carver")]
        public string OutputRoot { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Allow replace existing files", Order = 4, GroupName = "Carver")]
        public bool AllowReplaceExistingFiles { get; set; }

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Name = "CarverManifestDailyExporterPhase1";
                Description = "Disarmed Carver phase-1 MES/ZN/ZF daily Last export helper for source-native futures data.";
                Calculate = Calculate.OnBarClose;
                IsOverlay = true;
                DisplayInDataBox = false;
                DrawOnPricePanel = false;
                IsSuspendedWhileInactive = false;
                BarsRequiredToPlot = 0;

                ExecutionArmed = false;
                ExpectedManifestId = LockedManifestId;
                OutputRoot = LockedOutputRoot;
                AllowReplaceExistingFiles = false;
            }
            else if (State == State.DataLoaded)
            {
                ValidateConfiguration();
                if (!ExecutionArmed)
                {
                    Print("CARVER_PHASE1_MANIFEST_DAILY_EXPORT_PREPARED_NOT_ARMED rows=" + ManifestRows.Length.ToString(CultureInfo.InvariantCulture));
                    return;
                }
                StartManifestRequests();
            }
            else if (State == State.Terminated)
            {
                foreach (BarsRequest request in activeRequests)
                    request.Dispose();
                activeRequests.Clear();
            }
        }

        protected override void OnBarUpdate()
        {
            // This indicator has no trading, signal, diagnostic, or strategy logic.
        }

        private void ValidateConfiguration()
        {
            if (ExpectedManifestId != LockedManifestId)
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: manifest id drift.");

            string lockedRoot = Path.GetFullPath(LockedOutputRoot).TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            string requestedRoot = Path.GetFullPath(OutputRoot ?? string.Empty).TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            if (!string.Equals(requestedRoot, lockedRoot, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: output root must stay in the native daily quarantine.");

            foreach (ExportRow row in ManifestRows)
                ValidateRow(row);
        }

        private void ValidateRow(ExportRow row)
        {
            if (row.Root != "MES" && row.Root != "ZN" && row.Root != "ZF")
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: root is not in MES/ZN/ZF.");
            if (row.NinjaTraderSymbol != row.Root + " " + MonthCode(row.ContractMonth))
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: NinjaTrader symbol drift.");
            if (!row.NativeFile.Equals(row.Root + @"\" + row.Root + " " + row.ContractMonth + ".Last.txt", StringComparison.Ordinal))
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: native file drift.");
            ParseDate(row.StartDate);
            ParseDate(row.EndDate);
        }

        private void StartManifestRequests()
        {
            if (started)
                return;
            started = true;
            pendingRequests = ManifestRows.Length;

            foreach (ExportRow row in ManifestRows)
                RequestRow(row);
        }

        private void RequestRow(ExportRow row)
        {
            Instrument instrument = NinjaTrader.Cbi.Instrument.GetInstrument(row.NinjaTraderSymbol);
            if (instrument == null)
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: NinjaTrader instrument not found: " + row.NinjaTraderSymbol);

            BarsRequest request = new BarsRequest(instrument, ParseDate(row.StartDate), ParseDate(row.EndDate));
            request.BarsPeriod = new BarsPeriod { BarsPeriodType = BarsPeriodType.Day, Value = 1 };
            request.LookupPolicy = LookupPolicies.Provider;
            activeRequests.Add(request);

            request.Request(new Action<BarsRequest, ErrorCode, string>((bars, errorCode, errorMessage) =>
            {
                if (errorCode != ErrorCode.NoError)
                    throw new InvalidOperationException("Carver phase-1 manifest export blocked: bars request failed for " + row.NinjaTraderSymbol + ": " + errorCode + " " + errorMessage);

                WriteNativeExport(row, bars);
                pendingRequests -= 1;
                Print("CARVER_PHASE1_MANIFEST_DAILY_EXPORT_WRITTEN " + row.NativeFile + " pending=" + pendingRequests.ToString(CultureInfo.InvariantCulture));
            }));
        }

        private void WriteNativeExport(ExportRow row, BarsRequest bars)
        {
            string outputPath = Path.Combine(OutputRoot, row.NativeFile);
            string outputDirectory = Path.GetDirectoryName(outputPath);
            if (string.IsNullOrWhiteSpace(outputDirectory))
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: output directory missing.");
            Directory.CreateDirectory(outputDirectory);

            DateTime start = ParseDate(row.StartDate).Date;
            DateTime end = ParseDate(row.EndDate).Date;
            List<string> lines = new List<string>();
            for (int i = 0; i < bars.Bars.Count; i++)
            {
                DateTime tradeDate = bars.Bars.GetTime(i).Date;
                if (tradeDate < start || tradeDate > end)
                    continue;

                lines.Add(string.Join(";", new[]
                {
                    tradeDate.ToString("yyyyMMdd", CultureInfo.InvariantCulture),
                    bars.Bars.GetOpen(i).ToString("G17", CultureInfo.InvariantCulture),
                    bars.Bars.GetHigh(i).ToString("G17", CultureInfo.InvariantCulture),
                    bars.Bars.GetLow(i).ToString("G17", CultureInfo.InvariantCulture),
                    bars.Bars.GetClose(i).ToString("G17", CultureInfo.InvariantCulture),
                    bars.Bars.GetVolume(i).ToString(CultureInfo.InvariantCulture)
                }));
            }

            if (lines.Count == 0)
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: no completed daily rows returned for " + row.NinjaTraderSymbol);

            string tempPath = outputPath + ".tmp";
            if (File.Exists(tempPath))
                File.Delete(tempPath);
            if (File.Exists(outputPath) && !AllowReplaceExistingFiles)
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: target file exists and replacement is not explicitly allowed.");
            File.WriteAllLines(tempPath, lines);
            if (File.Exists(outputPath))
                File.Delete(outputPath);
            File.Move(tempPath, outputPath);
        }

        private static DateTime ParseDate(string value)
        {
            DateTime parsed;
            if (!DateTime.TryParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out parsed))
                throw new InvalidOperationException("Carver phase-1 manifest export blocked: date must use yyyy-MM-dd.");
            return parsed;
        }

        private static string MonthCode(string contractMonth)
        {
            if (contractMonth == "09-25")
                return "SEP25";
            if (contractMonth == "12-25")
                return "DEC25";
            if (contractMonth == "03-26")
                return "MAR26";
            if (contractMonth == "06-26")
                return "JUN26";
            throw new InvalidOperationException("Carver phase-1 manifest export blocked: undeclared contract month.");
        }
    }
}
