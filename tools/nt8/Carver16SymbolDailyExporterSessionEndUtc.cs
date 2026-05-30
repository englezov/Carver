// Locked 16-symbol NinjaTrader Desktop daily export helper for Carver.
// Defaults to disarmed. Import/run only under a separate operator execution gate.
// Requests only the hard-coded source-native manifest rows below, 1 Day Last bars,
// for completed trading dates 2026-05-18 through 2026-05-22. Output is helper
// raw output with template-derived UTC session-end timestamps, not provider-
// verbatim NinjaTrader Time[0] output.

#region Using declarations
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.IO;
using System.Linq;
using NinjaTrader.Cbi;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.Indicators;
#endregion

namespace NinjaTrader.NinjaScript.Indicators
{
    public class Carver16SymbolDailyExporterSessionEndUtc : Indicator
    {
        private const bool ExecutionArmed = false;
        private const bool AllowReplaceExistingFiles = false;
        private const string LockedManifestId = "CARVER_16_SYMBOL_DAILY_LAST_2026_05_18_TO_2026_05_22";
        private const string LockedBarType = "Last";
        private const string LockedTimeframe = "1 Day";
        private const string LockedTimestampPolicy = "HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0";
        private const string LockedOutputRoot = @"C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22";
        private const string LockedHelperRawFolder = "helper_raw_output";

        private static readonly DateTime LockedStartDate = new DateTime(2026, 5, 18);
        private static readonly DateTime LockedEndDate = new DateTime(2026, 5, 22);

        private readonly List<BarsRequest> activeRequests = new List<BarsRequest>();
        private readonly SortedDictionary<string, List<string>> collectedRowsBySymbol = new SortedDictionary<string, List<string>>(StringComparer.Ordinal);
        private readonly SortedDictionary<string, List<string>> availabilityFailuresBySymbol = new SortedDictionary<string, List<string>>(StringComparer.Ordinal);
        private readonly object requestLock = new object();
        private bool started;
        private bool wroteFiles;
        private int pendingRequests;

        private sealed class ExportRow
        {
            public string RowId { get; private set; }
            public string Symbol { get; private set; }
            public string ContractMonth { get; private set; }
            public string NinjaTraderSymbol { get; private set; }
            public string LocalContract { get; private set; }
            public string TradingHoursTemplate { get; private set; }
            public string TemplateTimeZoneId { get; private set; }
            public int SessionEndHour { get; private set; }
            public int SessionEndMinute { get; private set; }

            public ExportRow(
                string rowId,
                string symbol,
                string contractMonth,
                string ninjaTraderSymbol,
                string localContract,
                string tradingHoursTemplate,
                string templateTimeZoneId,
                int sessionEndHour,
                int sessionEndMinute)
            {
                RowId = rowId;
                Symbol = symbol;
                ContractMonth = contractMonth;
                NinjaTraderSymbol = ninjaTraderSymbol;
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
                    return Symbol + "_" + ContractMonth + "_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv";
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
                Name = "DEPRECATED_DO_NOT_USE_Carver16SymbolDailyExporterSessionEndUtc";
                Description = "Deprecated BarsRequest helper. Do not use for the 16-symbol test; use Carver16SymbolDailyChartSeriesExporterSessionEndUtc.";
                Calculate = Calculate.OnBarClose;
                IsOverlay = true;
                DisplayInDataBox = false;
                DrawOnPricePanel = false;
                IsSuspendedWhileInactive = false;
                BarsRequiredToPlot = 0;

                OperatorAcknowledgement = "DISARMED_BY_DEFAULT";
            }
            else if (State == State.DataLoaded)
            {
                ValidateConfiguration();
                collectedRowsBySymbol.Clear();
                availabilityFailuresBySymbol.Clear();
                wroteFiles = false;

                if (!ExecutionArmed)
                {
                    Print("CARVER_16_SYMBOL_DAILY_EXPORT_PREPARED_NOT_ARMED file_requires_ExecutionArmed_true rows=" + ManifestRows.Length.ToString(CultureInfo.InvariantCulture));
                    return;
                }

                if (OperatorAcknowledgement != "OPERATOR_AUTHORIZED_16_SYMBOL_DAILY_LAST_2026_05_18_TO_2026_05_22")
                    throw new InvalidOperationException("Carver 16-symbol export blocked: operator acknowledgement token is not set.");

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
            if (LockedManifestId != "CARVER_16_SYMBOL_DAILY_LAST_2026_05_18_TO_2026_05_22"
                || LockedBarType != "Last"
                || LockedTimeframe != "1 Day"
                || LockedTimestampPolicy != "HELPER_RAW_OUTPUT_WITH_TEMPLATE_DERIVED_UTC_SESSION_END_TIMESTAMPS_NOT_PROVIDER_VERBATIM_TIME0")
                throw new InvalidOperationException("Carver 16-symbol export blocked: locked identity fields drifted.");

            string lockedRoot = Path.GetFullPath(LockedOutputRoot)
                .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            string requiredRoot = Path.GetFullPath(@"C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\16_SYMBOL_DAILY_LAST_2026-05-18_2026-05-22")
                .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            if (!string.Equals(lockedRoot, requiredRoot, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("Carver 16-symbol export blocked: output root drifted.");

            if (ManifestRows.Length != 16)
                throw new InvalidOperationException("Carver 16-symbol export blocked: manifest row count drifted.");

            HashSet<string> rowIds = new HashSet<string>(StringComparer.Ordinal);
            HashSet<string> symbols = new HashSet<string>(StringComparer.Ordinal);
            foreach (ExportRow row in ManifestRows)
                ValidateRow(row, rowIds, symbols);

            if (rowIds.Count != 16 || symbols.Count != 16)
                throw new InvalidOperationException("Carver 16-symbol export blocked: duplicate manifest row ids or symbols.");
        }

        private void ValidateRow(ExportRow row, HashSet<string> rowIds, HashSet<string> symbols)
        {
            if (!rowIds.Add(row.RowId))
                throw new InvalidOperationException("Carver 16-symbol export blocked: duplicate row id " + row.RowId);
            if (!symbols.Add(row.Symbol))
                throw new InvalidOperationException("Carver 16-symbol export blocked: duplicate symbol " + row.Symbol);
            if (row.NinjaTraderSymbol != row.Symbol + " " + MonthCode(row.ContractMonth))
                throw new InvalidOperationException("Carver 16-symbol export blocked: NinjaTrader symbol drift for " + row.Symbol);
            if (row.LocalContract != row.Symbol + " " + row.ContractMonth)
                throw new InvalidOperationException("Carver 16-symbol export blocked: local contract drift for " + row.Symbol);
            if (!IsAllowedSymbolAndContract(row.Symbol, row.ContractMonth))
                throw new InvalidOperationException("Carver 16-symbol export blocked: undeclared symbol/contract " + row.Symbol + " " + row.ContractMonth);
            ParseDate("2026-05-18");
            ParseDate("2026-05-22");
            TimeZoneInfo.FindSystemTimeZoneById(row.TemplateTimeZoneId);
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
                throw new InvalidOperationException("Carver 16-symbol export blocked: NinjaTrader instrument not found: " + row.NinjaTraderSymbol);

            BarsRequest request = new BarsRequest(instrument, LockedStartDate, LockedEndDate);
            request.BarsPeriod = new BarsPeriod
            {
                BarsPeriodType = BarsPeriodType.Day,
                Value = 1,
                MarketDataType = MarketDataType.Last
            };
            request.LookupPolicy = LookupPolicies.Provider;
            activeRequests.Add(request);

            request.Request(new Action<BarsRequest, ErrorCode, string>((bars, errorCode, errorMessage) =>
            {
                lock (requestLock)
                {
                    if (errorCode != ErrorCode.NoError)
                    {
                        availabilityFailuresBySymbol[row.Symbol] = new List<string>
                        {
                            "bars request failed for " + row.NinjaTraderSymbol + ": " + errorCode + " " + errorMessage
                        };
                    }
                    else
                    {
                        RowBuildResult result = BuildRows(row, bars);
                        if (result.Failures.Count == 0)
                        {
                            collectedRowsBySymbol[row.Symbol] = result.Rows;
                            Print("CARVER_16_SYMBOL_DAILY_EXPORT_COLLECTED " + row.NinjaTraderSymbol);
                        }
                        else
                        {
                            availabilityFailuresBySymbol[row.Symbol] = result.Failures;
                            Print("CARVER_16_SYMBOL_DAILY_EXPORT_PREFLIGHT_BLOCKED " + row.NinjaTraderSymbol + " failures=" + result.Failures.Count.ToString(CultureInfo.InvariantCulture));
                        }
                    }

                    pendingRequests -= 1;
                    Print("CARVER_16_SYMBOL_DAILY_EXPORT_PENDING " + pendingRequests.ToString(CultureInfo.InvariantCulture));

                    if (pendingRequests == 0)
                        WriteAllExportsIfReady();
                }
            }));
        }

        private sealed class RowBuildResult
        {
            public List<string> Rows { get; private set; }
            public List<string> Failures { get; private set; }

            public RowBuildResult(List<string> rows, List<string> failures)
            {
                Rows = rows;
                Failures = failures;
            }
        }

        private RowBuildResult BuildRows(ExportRow row, BarsRequest bars)
        {
            SortedDictionary<DateTime, string> rowsByDate = new SortedDictionary<DateTime, string>();
            List<string> failures = new List<string>();
            for (int i = 0; i < bars.Bars.Count; i++)
            {
                DateTime tradeDate = bars.Bars.GetTime(i).Date;
                if (tradeDate < LockedStartDate || tradeDate > LockedEndDate)
                {
                    failures.Add(row.NinjaTraderSymbol + " row outside locked date window date=" + FormatDate(tradeDate));
                    continue;
                }
                if (rowsByDate.ContainsKey(tradeDate))
                {
                    failures.Add(row.NinjaTraderSymbol + " duplicate completed daily bar date=" + FormatDate(tradeDate));
                    continue;
                }

                rowsByDate.Add(tradeDate, string.Join(",", new[]
                {
                    row.RowId,
                    row.Symbol,
                    row.LocalContract,
                    FormatTemplateSessionEndUtc(row, tradeDate),
                    FormatDate(tradeDate),
                    bars.Bars.GetOpen(i).ToString("G17", CultureInfo.InvariantCulture),
                    bars.Bars.GetHigh(i).ToString("G17", CultureInfo.InvariantCulture),
                    bars.Bars.GetLow(i).ToString("G17", CultureInfo.InvariantCulture),
                    bars.Bars.GetClose(i).ToString("G17", CultureInfo.InvariantCulture),
                    bars.Bars.GetVolume(i).ToString(CultureInfo.InvariantCulture),
                    row.TradingHoursTemplate,
                    LockedTimestampPolicy
                }));
            }

            foreach (DateTime expectedDate in ExpectedDates())
            {
                if (!rowsByDate.ContainsKey(expectedDate))
                    failures.Add(row.NinjaTraderSymbol + " missing completed daily bar date=" + FormatDate(expectedDate));
            }

            if (rowsByDate.Count != 5)
                failures.Add(row.NinjaTraderSymbol + " expected exactly five completed daily rows but collected=" + rowsByDate.Count.ToString(CultureInfo.InvariantCulture));

            return new RowBuildResult(rowsByDate.Values.ToList(), failures);
        }

        private void WriteAllExportsIfReady()
        {
            if (wroteFiles)
                return;
            if (availabilityFailuresBySymbol.Count > 0)
                ThrowAvailabilityPreflightFailure();
            if (collectedRowsBySymbol.Count != 16)
                throw new InvalidOperationException("Carver 16-symbol export blocked: not all manifest rows collected.");
            foreach (ExportRow row in ManifestRows)
            {
                if (!collectedRowsBySymbol.ContainsKey(row.Symbol) || collectedRowsBySymbol[row.Symbol].Count != 5)
                    throw new InvalidOperationException("Carver 16-symbol export blocked: collected row count drift for " + row.Symbol);
            }

            string outputDirectory = Path.Combine(LockedOutputRoot, LockedHelperRawFolder);
            Directory.CreateDirectory(outputDirectory);

            Dictionary<ExportRow, string> outputPathsByRow = new Dictionary<ExportRow, string>();
            Dictionary<ExportRow, string> tempPathsByRow = new Dictionary<ExportRow, string>();
            foreach (ExportRow row in ManifestRows)
            {
                string outputPath = Path.Combine(outputDirectory, row.OutputFileName);
                string tempPath = outputPath + ".tmp";
                if (File.Exists(outputPath) && !AllowReplaceExistingFiles)
                    throw new InvalidOperationException("Carver 16-symbol export blocked: target file already exists and replacement is disabled: " + outputPath);
                if (File.Exists(tempPath))
                    throw new InvalidOperationException("Carver 16-symbol export blocked: temp file already exists before write preflight: " + tempPath);

                outputPathsByRow[row] = outputPath;
                tempPathsByRow[row] = tempPath;
            }

            foreach (ExportRow row in ManifestRows)
            {
                string header = "row_id,provider_symbol,local_contract,timestamp_utc,completed_trading_date,open,high,low,close,volume,trading_hours_template,helper_timestamp_policy";
                string tempPath = tempPathsByRow[row];
                File.WriteAllLines(tempPath, new[] { header }.Concat(collectedRowsBySymbol[row.Symbol]));
            }

            foreach (ExportRow row in ManifestRows)
            {
                string outputPath = outputPathsByRow[row];
                string tempPath = tempPathsByRow[row];
                if (File.Exists(outputPath))
                    File.Delete(outputPath);
                File.Move(tempPath, outputPath);
                Print("CARVER_16_SYMBOL_DAILY_EXPORT_WRITTEN " + outputPath);
            }

            wroteFiles = true;
        }

        private void ThrowAvailabilityPreflightFailure()
        {
            List<string> allFailures = new List<string>();
            foreach (KeyValuePair<string, List<string>> entry in availabilityFailuresBySymbol)
            {
                foreach (string failure in entry.Value)
                {
                    string reportLine = entry.Key + ": " + failure;
                    allFailures.Add(reportLine);
                    Print("CARVER_16_SYMBOL_DAILY_EXPORT_AVAILABILITY_FAILURE " + reportLine);
                }
            }

            throw new InvalidOperationException(
                "Carver 16-symbol export blocked: availability preflight failed before any helper raw-output write. failures="
                + allFailures.Count.ToString(CultureInfo.InvariantCulture)
                + " details="
                + string.Join(" | ", allFailures));
        }

        private static IEnumerable<DateTime> ExpectedDates()
        {
            for (DateTime current = LockedStartDate; current <= LockedEndDate; current = current.AddDays(1))
                yield return current;
        }

        private static DateTime ParseDate(string value)
        {
            DateTime parsed;
            if (!DateTime.TryParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out parsed))
                throw new InvalidOperationException("Carver 16-symbol export blocked: date must use yyyy-MM-dd.");
            return parsed;
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

        private static string MonthCode(string contractMonth)
        {
            if (contractMonth == "06-26")
                return "JUN26";
            if (contractMonth == "07-26")
                return "JUL26";
            throw new InvalidOperationException("Carver 16-symbol export blocked: undeclared contract month.");
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
    }
}
