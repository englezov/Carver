// Locked 16-symbol NinjaTrader Desktop full-history daily chart/AddDataSeries export helper for Carver.
// Defaults to disarmed. Import/run only under a separate operator execution gate.
// Attach to a 1 Day Last chart for one of the locked manifest contracts. The helper
// adds the exact 16 source-native dated contracts below, collects all loaded
// historical completed daily bars for those contracts, and writes helper raw output
// with template-derived UTC session-end timestamps, not provider-verbatim
// NinjaTrader Time[0] output.

#region Using declarations
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.IO;
using System.Linq;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.Indicators;
#endregion

namespace NinjaTrader.NinjaScript.Indicators
{
    public class CarveDD : Indicator
    {
        private const bool ExecutionArmed = false;
        private const bool AllowReplaceExistingFiles = false;
        private const string LockedManifestId = "CARVER_16_SYMBOL_FULL_DAILY_HISTORY_DAILY_LAST";
        private const string LockedBarType = "Last";
        private const string LockedTimeframe = "1 Day";
        private const string LockedTimestampPolicy = "HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0";
        private const string LockedOutputRoot = @"C:\Users\openclaw\Desktop\Carver\q\nt16fh";
        private const string LockedHelperRawFolder = "raw_market_files";
        private const string LockedProviderMetadataFolder = "provider_metadata";

        private readonly SortedDictionary<string, SortedDictionary<DateTime, string>> rowsBySymbol =
            new SortedDictionary<string, SortedDictionary<DateTime, string>>(StringComparer.Ordinal);
        private readonly SortedDictionary<string, List<string>> availabilityFailuresBySymbol =
            new SortedDictionary<string, List<string>>(StringComparer.Ordinal);
        private bool wroteFiles;

        private sealed class ExportRow
        {
            public string RowId { get; private set; }
            public string Symbol { get; private set; }
            public string ContractMonth { get; private set; }
            public string NinjaTraderContract { get; private set; }
            public string LocalContract { get; private set; }
            public string TradingHoursTemplate { get; private set; }
            public string TemplateTimeZoneId { get; private set; }
            public int SessionEndHour { get; private set; }
            public int SessionEndMinute { get; private set; }

            public ExportRow(
                string rowId,
                string symbol,
                string contractMonth,
                string ninjaTraderContract,
                string localContract,
                string tradingHoursTemplate,
                string templateTimeZoneId,
                int sessionEndHour,
                int sessionEndMinute)
            {
                RowId = rowId;
                Symbol = symbol;
                ContractMonth = contractMonth;
                NinjaTraderContract = ninjaTraderContract;
                LocalContract = localContract;
                TradingHoursTemplate = tradingHoursTemplate;
                TemplateTimeZoneId = templateTimeZoneId;
                SessionEndHour = sessionEndHour;
                SessionEndMinute = sessionEndMinute;
            }

            public string OutputFileName
            {
                get
                {
                    return Symbol + "_" + ContractMonth + "_Daily_Last_FULL_HISTORY_TEMPLATE_SESSION_END_UTC_HELPER_RAW.csv";
                }
            }
        }

        private static readonly ExportRow[] ManifestRows = new[]
        {
            new ExportRow("APPENDIX_C_172_001", "ZT", "06-26", "ZT JUN26", "ZT 06-26", "CBOT Interest Rate ETH", "Central Standard Time", 16, 0),
            new ExportRow("APPENDIX_C_172_003", "ZF", "06-26", "ZF JUN26", "ZF 06-26", "CBOT Interest Rate ETH", "Central Standard Time", 16, 0),
            new ExportRow("APPENDIX_C_172_004", "ZN", "06-26", "ZN JUN26", "ZN 06-26", "CBOT Interest Rate ETH", "Central Standard Time", 16, 0),
            new ExportRow("APPENDIX_C_174_006", "MES", "06-26", "MES JUN26", "MES 06-26", "CME US Index Futures ETH", "Central Standard Time", 16, 0),
            new ExportRow("APPENDIX_C_174_002", "MNQ", "06-26", "MNQ JUN26", "MNQ 06-26", "CME US Index Futures ETH", "Central Standard Time", 16, 0),
            new ExportRow("APPENDIX_C_174_004", "M2K", "06-26", "M2K JUN26", "M2K 06-26", "CME US Index Futures ETH", "Central Standard Time", 16, 0),
            new ExportRow("APPENDIX_C_174_001", "MYM", "06-26", "MYM JUN26", "MYM 06-26", "CME US Index Futures ETH", "Central Standard Time", 16, 0),
            new ExportRow("APPENDIX_C_182_002", "QM", "07-26", "QM JUL26", "QM 07-26", "Nymex Metals - Energy ETH", "Eastern Standard Time", 17, 0),
            new ExportRow("APPENDIX_C_182_004", "RB", "07-26", "RB JUL26", "RB 07-26", "Nymex Metals - Energy ETH", "Eastern Standard Time", 17, 0),
            new ExportRow("APPENDIX_C_183_003", "ZC", "07-26", "ZC JUL26", "ZC 07-26", "CBOT Agriculturals ETH", "Central Standard Time", 13, 20),
            new ExportRow("APPENDIX_C_183_010", "ZS", "07-26", "ZS JUL26", "ZS 07-26", "CBOT Agriculturals ETH", "Central Standard Time", 13, 20),
            new ExportRow("APPENDIX_C_183_011", "ZM", "07-26", "ZM JUL26", "ZM 07-26", "CBOT Agriculturals ETH", "Central Standard Time", 13, 20),
            new ExportRow("APPENDIX_C_183_012", "ZL", "07-26", "ZL JUL26", "ZL 07-26", "CBOT Agriculturals ETH", "Central Standard Time", 13, 20),
            new ExportRow("APPENDIX_C_183_013", "ZW", "07-26", "ZW JUL26", "ZW 07-26", "CBOT Agriculturals ETH", "Central Standard Time", 13, 20),
            new ExportRow("APPENDIX_C_183_005", "HE", "06-26", "HE JUN26", "HE 06-26", "CME Commodities ETH", "Central Standard Time", 13, 5),
            new ExportRow("APPENDIX_C_183_006", "LE", "06-26", "LE JUN26", "LE 06-26", "CME Commodities ETH", "Central Standard Time", 13, 5),
        };

        [NinjaScriptProperty]
        [Display(Name = "Operator acknowledgement", Order = 1, GroupName = "Carver")]
        public string OperatorAcknowledgement { get; set; }

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Name = "CarveDD";
                Description = "Disarmed CarveDD 16-symbol full-history daily Last chart/AddDataSeries export helper with template session-end UTC timestamps.";
                Calculate = Calculate.OnBarClose;
                IsOverlay = true;
                DisplayInDataBox = false;
                DrawOnPricePanel = false;
                IsSuspendedWhileInactive = false;
                BarsRequiredToPlot = 0;

                OperatorAcknowledgement = "DISARMED_BY_DEFAULT";
            }
            else if (State == State.Configure)
            {
                if (!ExecutionArmed)
                    return;

                foreach (ExportRow row in ManifestRows)
                    AddDataSeries(row.NinjaTraderContract, BarsPeriodType.Day, 1, MarketDataType.Last);
            }
            else if (State == State.DataLoaded)
            {
                ValidateConfiguration();
                rowsBySymbol.Clear();
                availabilityFailuresBySymbol.Clear();
                wroteFiles = false;
                foreach (ExportRow row in ManifestRows)
                    rowsBySymbol[row.Symbol] = new SortedDictionary<DateTime, string>();

                if (!ExecutionArmed)
                {
                    Print("CARVER_16_SYMBOL_CHART_SERIES_EXPORT_PREPARED_NOT_ARMED file_requires_ExecutionArmed_true rows=" + ManifestRows.Length.ToString(CultureInfo.InvariantCulture));
                    return;
                }

                if (OperatorAcknowledgement != "OPERATOR_AUTHORIZED_16_SYMBOL_FULL_DAILY_HISTORY_DAILY_LAST_QUARANTINE")
                    throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: operator acknowledgement token is not set.");
            }
            else if (State == State.Realtime)
            {
                if (ExecutionArmed && !wroteFiles)
                    WriteAllExportsIfReady();
            }
        }

        protected override void OnBarUpdate()
        {
            if (!ExecutionArmed || wroteFiles || BarsInProgress == 0)
                return;

            int manifestIndex = BarsInProgress - 1;
            if (manifestIndex < 0 || manifestIndex >= ManifestRows.Length)
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: BarsInProgress drifted.");

            ExportRow row = ManifestRows[manifestIndex];
            ValidateLoadedSeriesTemplate(BarsInProgress, row);
            DateTime tradeDate = Times[BarsInProgress][0].Date;

            SortedDictionary<DateTime, string> targetRows = rowsBySymbol[row.Symbol];
            if (targetRows.ContainsKey(tradeDate))
            {
                RecordFailure(row.Symbol, row.NinjaTraderContract + " duplicate completed daily bar date=" + FormatDate(tradeDate));
                return;
            }

            targetRows.Add(tradeDate, ToCsvRow(row, tradeDate));
            Print("CARVER_16_SYMBOL_CHART_SERIES_EXPORT_COLLECTED " + row.NinjaTraderContract + " date=" + FormatDate(tradeDate));
        }

        private void ValidateConfiguration()
        {
            if (LockedManifestId != "CARVER_16_SYMBOL_FULL_DAILY_HISTORY_DAILY_LAST"
                || LockedBarType != "Last"
                || LockedTimeframe != "1 Day"
                || LockedTimestampPolicy != "HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0")
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: locked identity fields drifted.");

            if (Instrument == null || !IsAllowedPrimaryInstrument(Instrument.FullName))
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: attach only to one of the locked manifest dated contracts.");

            if (BarsPeriod == null || BarsPeriod.BarsPeriodType != BarsPeriodType.Day || BarsPeriod.Value != 1)
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: primary chart must use 1 Day bars.");

            if (BarsPeriod.MarketDataType != MarketDataType.Last)
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: primary chart must use Last bars.");

            string lockedRoot = Path.GetFullPath(LockedOutputRoot)
                .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            string requiredRoot = Path.GetFullPath(@"C:\Users\openclaw\Desktop\Carver\q\nt16fh")
                .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            if (!string.Equals(lockedRoot, requiredRoot, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: output root drifted.");

            if (ManifestRows.Length != 16)
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: manifest row count drifted.");

            HashSet<string> rowIds = new HashSet<string>(StringComparer.Ordinal);
            HashSet<string> symbols = new HashSet<string>(StringComparer.Ordinal);
            foreach (ExportRow row in ManifestRows)
                ValidateRow(row, rowIds, symbols);

            if (rowIds.Count != 16 || symbols.Count != 16)
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: duplicate manifest row ids or symbols.");

            ValidateLoadedSeriesTemplate(0, FindManifestRowByContract(Instrument.FullName));
        }

        private void ValidateRow(ExportRow row, HashSet<string> rowIds, HashSet<string> symbols)
        {
            if (!rowIds.Add(row.RowId))
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: duplicate row id " + row.RowId);
            if (!symbols.Add(row.Symbol))
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: duplicate symbol " + row.Symbol);
            if (row.NinjaTraderContract != row.Symbol + " " + MonthCode(row.ContractMonth))
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: NinjaTrader contract drift for " + row.Symbol);
            if (row.LocalContract != row.Symbol + " " + row.ContractMonth)
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: local contract drift for " + row.Symbol);
            if (!IsAllowedSymbolAndContract(row.Symbol, row.ContractMonth))
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: undeclared symbol/contract " + row.Symbol + " " + row.ContractMonth);
            TimeZoneInfo.FindSystemTimeZoneById(row.TemplateTimeZoneId);
        }

        private void ValidateLoadedSeriesTemplate(int barsArrayIndex, ExportRow row)
        {
            if (BarsArray == null || barsArrayIndex < 0 || barsArrayIndex >= BarsArray.Length || BarsArray[barsArrayIndex] == null || BarsArray[barsArrayIndex].TradingHours == null)
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: unable to verify loaded trading-hours template for " + row.LocalContract);

            string actualTemplate = BarsArray[barsArrayIndex].TradingHours.Name;
            if (!string.Equals(actualTemplate, row.TradingHoursTemplate, StringComparison.Ordinal))
                throw new InvalidOperationException(
                    "Carver 16-symbol chart-series export blocked: loaded trading-hours template mismatch for "
                    + row.LocalContract
                    + " expected="
                    + row.TradingHoursTemplate
                    + " actual="
                    + actualTemplate);
        }

        private string ToCsvRow(ExportRow row, DateTime tradeDate)
        {
            return string.Join(",", new[]
            {
                row.RowId,
                row.Symbol,
                row.LocalContract,
                FormatTemplateSessionEndUtc(row, tradeDate),
                FormatDate(tradeDate),
                Opens[BarsInProgress][0].ToString("G17", CultureInfo.InvariantCulture),
                Highs[BarsInProgress][0].ToString("G17", CultureInfo.InvariantCulture),
                Lows[BarsInProgress][0].ToString("G17", CultureInfo.InvariantCulture),
                Closes[BarsInProgress][0].ToString("G17", CultureInfo.InvariantCulture),
                Volumes[BarsInProgress][0].ToString(CultureInfo.InvariantCulture),
                row.TradingHoursTemplate,
                LockedTimestampPolicy
            });
        }

        private void RecordFailure(string symbol, string failure)
        {
            if (!availabilityFailuresBySymbol.ContainsKey(symbol))
                availabilityFailuresBySymbol[symbol] = new List<string>();
            availabilityFailuresBySymbol[symbol].Add(failure);
            Print("CARVER_16_SYMBOL_CHART_SERIES_EXPORT_AVAILABILITY_FAILURE " + symbol + ": " + failure);
        }

        private void WriteAllExportsIfReady()
        {
            if (wroteFiles)
                return;

            CollectZeroRowFailures();

            string outputDirectory = Path.Combine(LockedOutputRoot, LockedHelperRawFolder);
            string metadataDirectory = Path.Combine(LockedOutputRoot, LockedProviderMetadataFolder);
            Directory.CreateDirectory(outputDirectory);
            Directory.CreateDirectory(metadataDirectory);

            Dictionary<ExportRow, string> outputPathsByRow = new Dictionary<ExportRow, string>();
            Dictionary<ExportRow, string> tempPathsByRow = new Dictionary<ExportRow, string>();
            foreach (ExportRow row in ManifestRows)
            {
                if (!rowsBySymbol.ContainsKey(row.Symbol) || rowsBySymbol[row.Symbol].Count == 0)
                    continue;

                string outputPath = Path.Combine(outputDirectory, row.OutputFileName);
                string tempPath = outputPath + ".tmp";
                if (File.Exists(outputPath) && !AllowReplaceExistingFiles)
                    throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: target file already exists and replacement is disabled: " + outputPath);
                if (File.Exists(tempPath))
                    throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: temp file already exists before write preflight: " + tempPath);

                outputPathsByRow[row] = outputPath;
                tempPathsByRow[row] = tempPath;
            }

            string availabilityPath = Path.Combine(metadataDirectory, "NINJATRADER_16_SYMBOL_FULL_DAILY_HISTORY_HELPER_AVAILABILITY_REPORT.csv");
            string availabilityTempPath = availabilityPath + ".tmp";
            if (File.Exists(availabilityPath) && !AllowReplaceExistingFiles)
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: availability report already exists and replacement is disabled: " + availabilityPath);
            if (File.Exists(availabilityTempPath))
                throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: availability temp file already exists before write preflight: " + availabilityTempPath);

            List<string> movedOutputPaths = new List<string>();
            try
            {
                foreach (ExportRow row in ManifestRows)
                {
                    if (!tempPathsByRow.ContainsKey(row))
                        continue;

                    string header = "row_id,provider_symbol,local_contract,timestamp_utc,completed_trading_date,open,high,low,close,volume,trading_hours_template,helper_timestamp_policy";
                    string tempPath = tempPathsByRow[row];
                    File.WriteAllLines(tempPath, new[] { header }.Concat(rowsBySymbol[row.Symbol].Values));
                }

                File.WriteAllLines(availabilityTempPath, BuildAvailabilityReportRows());

                foreach (ExportRow row in ManifestRows)
                {
                    if (!outputPathsByRow.ContainsKey(row))
                        continue;

                    string outputPath = outputPathsByRow[row];
                    string tempPath = tempPathsByRow[row];
                    if (File.Exists(outputPath))
                        File.Delete(outputPath);
                    File.Move(tempPath, outputPath);
                    movedOutputPaths.Add(outputPath);
                    Print("CARVER_16_SYMBOL_CHART_SERIES_EXPORT_WRITTEN " + outputPath);
                }

                if (File.Exists(availabilityPath))
                    File.Delete(availabilityPath);
                File.Move(availabilityTempPath, availabilityPath);
                movedOutputPaths.Add(availabilityPath);
                Print("CARVER_16_SYMBOL_CHART_SERIES_EXPORT_AVAILABILITY_REPORT_WRITTEN " + availabilityPath);
            }
            catch
            {
                foreach (string outputPath in movedOutputPaths)
                {
                    if (File.Exists(outputPath))
                        File.Delete(outputPath);
                }

                foreach (string tempPath in tempPathsByRow.Values)
                {
                    if (File.Exists(tempPath))
                        File.Delete(tempPath);
                }

                if (File.Exists(availabilityTempPath))
                    File.Delete(availabilityTempPath);

                throw;
            }

            wroteFiles = true;
        }

        private void CollectZeroRowFailures()
        {
            foreach (ExportRow row in ManifestRows)
            {
                SortedDictionary<DateTime, string> targetRows = rowsBySymbol.ContainsKey(row.Symbol)
                    ? rowsBySymbol[row.Symbol]
                    : new SortedDictionary<DateTime, string>();

                if (targetRows.Count == 0)
                    RecordFailure(row.Symbol, row.NinjaTraderContract + " returned zero loaded completed daily bars for full-history helper attempt");
            }
        }

        private IEnumerable<string> BuildAvailabilityReportRows()
        {
            yield return "row_id,provider_symbol,local_contract,ninjatrader_contract,row_count,first_completed_trading_date,last_completed_trading_date,status,failures";

            foreach (ExportRow row in ManifestRows)
            {
                SortedDictionary<DateTime, string> targetRows = rowsBySymbol.ContainsKey(row.Symbol)
                    ? rowsBySymbol[row.Symbol]
                    : new SortedDictionary<DateTime, string>();
                List<string> failures = availabilityFailuresBySymbol.ContainsKey(row.Symbol)
                    ? availabilityFailuresBySymbol[row.Symbol]
                    : new List<string>();

                string firstDate = targetRows.Count == 0 ? "" : FormatDate(targetRows.Keys.First());
                string lastDate = targetRows.Count == 0 ? "" : FormatDate(targetRows.Keys.Last());
                string status = targetRows.Count == 0
                    ? "BLOCKED_PROVIDER_UNAVAILABLE_OR_NOT_LOADED"
                    : (failures.Count == 0 ? "ACCEPTED_QUARANTINE_HELPER_RAW_AVAILABLE" : "ACCEPTED_WITH_RECORDED_AVAILABILITY_FAILURES");

                yield return string.Join(",", new[]
                {
                    row.RowId,
                    row.Symbol,
                    row.LocalContract,
                    row.NinjaTraderContract,
                    targetRows.Count.ToString(CultureInfo.InvariantCulture),
                    firstDate,
                    lastDate,
                    status,
                    QuoteCsv(string.Join(" | ", failures))
                });
            }
        }

        private static string FormatDate(DateTime value)
        {
            return value.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);
        }

        private static string FormatTemplateSessionEndUtc(ExportRow row, DateTime tradingDay)
        {
            TimeZoneInfo templateTimeZone = TimeZoneInfo.FindSystemTimeZoneById(row.TemplateTimeZoneId);
            DateTime localSessionEnd = DateTime.SpecifyKind(
                new DateTime(tradingDay.Year, tradingDay.Month, tradingDay.Day, row.SessionEndHour, row.SessionEndMinute, 0),
                DateTimeKind.Unspecified);
            DateTime utcSessionEnd = TimeZoneInfo.ConvertTimeToUtc(localSessionEnd, templateTimeZone);
            return utcSessionEnd.ToString("yyyy-MM-dd'T'HH:mm:ss'Z'", CultureInfo.InvariantCulture);
        }

        private static string QuoteCsv(string value)
        {
            if (value == null)
                value = "";
            return "\"" + value.Replace("\"", "\"\"") + "\"";
        }

        private static string MonthCode(string contractMonth)
        {
            if (contractMonth == "06-26")
                return "JUN26";
            if (contractMonth == "07-26")
                return "JUL26";
            throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: undeclared contract month.");
        }

        private static bool IsAllowedSymbolAndContract(string symbol, string contractMonth)
        {
            if ((symbol == "ZT" || symbol == "ZF" || symbol == "ZN" || symbol == "MES" || symbol == "MNQ" || symbol == "M2K" || symbol == "MYM" || symbol == "HE" || symbol == "LE")
                && contractMonth == "06-26")
                return true;

            if ((symbol == "QM" || symbol == "RB" || symbol == "ZC" || symbol == "ZS" || symbol == "ZM" || symbol == "ZL" || symbol == "ZW")
                && contractMonth == "07-26")
                return true;

            return false;
        }

        private static bool IsAllowedPrimaryInstrument(string fullName)
        {
            foreach (ExportRow row in ManifestRows)
            {
                if (string.Equals(fullName, row.NinjaTraderContract, StringComparison.Ordinal))
                    return true;
            }
            return false;
        }

        private static ExportRow FindManifestRowByContract(string fullName)
        {
            foreach (ExportRow row in ManifestRows)
            {
                if (string.Equals(fullName, row.NinjaTraderContract, StringComparison.Ordinal))
                    return row;
            }

            throw new InvalidOperationException("Carver 16-symbol chart-series export blocked: primary contract not found in manifest.");
        }
    }
}
