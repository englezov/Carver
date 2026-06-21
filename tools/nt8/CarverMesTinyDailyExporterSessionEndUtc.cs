// Locked MES-only NinjaTrader Desktop daily export helper for Carver.
// Defaults to disarmed. Import/run only under a separate operator execution gate.
// Attach to a 1 Day Last MES 06-26 chart. Writes only the five locked dates
// with template-derived session-end UTC timestamps. Output is helper raw
// output, not provider-verbatim NinjaTrader Time[0] output.

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
    public class CarverMesTinyDailyExporterSessionEndUtc : Indicator
    {
        private const bool ExecutionArmed = false;
        private const bool AllowReplaceExistingFile = false;
        private const string LockedNinjaTraderInstrumentFullName = "MES JUN26";
        private const string LockedProviderSymbol = "MES";
        private const string LockedLocalContract = "MES 06-26";
        private const string LockedBarType = "Last";
        private const string LockedTimeframe = "1 Day";
        private const string LockedTemplateTimeZoneId = "Central Standard Time";
        private const string LockedOutputDirectory = @"C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\MES_06_26_2026-05-18_2026-05-22\raw_source_copy";
        private const string LockedOutputFileName = "MES_06-26_Daily_Last_2026-05-18_2026-05-22_TEMPLATE_SESSION_END_UTC.csv";

        private static readonly DateTime LockedStartDate = new DateTime(2026, 5, 18);
        private static readonly DateTime LockedEndDate = new DateTime(2026, 5, 22);

        private readonly SortedDictionary<DateTime, string> rowsByTradeDate = new SortedDictionary<DateTime, string>();
        private bool wroteFile;

        [NinjaScriptProperty]
        [Display(Name = "Operator acknowledgement", Order = 1, GroupName = "Carver")]
        public string OperatorAcknowledgement { get; set; }

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Name = "CarverMesTinyDailyExporterSessionEndUtc";
                Description = "Disarmed Carver MES 06-26 five-day daily Last export helper with template session-end UTC timestamps.";
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
                rowsByTradeDate.Clear();
                wroteFile = false;
                ValidateConfiguration();

                if (!ExecutionArmed)
                {
                    Print("CARVER_MES_TINY_DAILY_EXPORT_PREPARED_NOT_ARMED file_requires_ExecutionArmed_true");
                    return;
                }

                if (OperatorAcknowledgement != "OPERATOR_AUTHORIZED_MES_06_26_2026_05_18_TO_2026_05_22")
                    throw new InvalidOperationException("Carver MES tiny export blocked: operator acknowledgement token is not set.");
            }
        }

        protected override void OnBarUpdate()
        {
            if (!ExecutionArmed || wroteFile || CurrentBar < 0)
                return;

            DateTime tradeDate = Time[0].Date;
            if (tradeDate < LockedStartDate)
                return;

            if (tradeDate > LockedEndDate)
            {
                WriteExportIfReady();
                return;
            }

            if (rowsByTradeDate.ContainsKey(tradeDate))
                throw new InvalidOperationException("Carver MES tiny export blocked: duplicate daily bar for " + FormatDate(tradeDate) + ".");

            rowsByTradeDate.Add(tradeDate, ToCsvRow(tradeDate));

            if (tradeDate == LockedEndDate)
                WriteExportIfReady();
        }

        private void ValidateConfiguration()
        {
            if (Instrument == null || Instrument.FullName != LockedNinjaTraderInstrumentFullName)
                throw new InvalidOperationException("Carver MES tiny export blocked: attach only to MES JUN26.");

            if (BarsPeriod == null || BarsPeriod.BarsPeriodType != BarsPeriodType.Day || BarsPeriod.Value != 1)
                throw new InvalidOperationException("Carver MES tiny export blocked: chart must use 1 Day bars.");

            if (BarsPeriod.MarketDataType != MarketDataType.Last)
                throw new InvalidOperationException("Carver MES tiny export blocked: chart must use Last bars.");

            if (LockedProviderSymbol != "MES"
                || LockedLocalContract != "MES 06-26"
                || LockedBarType != "Last"
                || LockedTimeframe != "1 Day"
                || LockedTemplateTimeZoneId != "Central Standard Time")
                throw new InvalidOperationException("Carver MES tiny export blocked: locked identity fields drifted.");

            string lockedRoot = Path.GetFullPath(LockedOutputDirectory)
                .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            string requiredRoot = Path.GetFullPath(@"C:\Users\openclaw\Desktop\Carver\docs\researchops\first_data_intake\quarantine\MES_06_26_2026-05-18_2026-05-22\raw_source_copy")
                .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            if (!string.Equals(lockedRoot, requiredRoot, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("Carver MES tiny export blocked: output root drifted.");
        }

        private string ToCsvRow(DateTime tradeDate)
        {
            return string.Join(",", new[]
            {
                LockedProviderSymbol,
                LockedLocalContract,
                FormatTemplateSessionEndUtc(tradeDate),
                Open[0].ToString("G17", CultureInfo.InvariantCulture),
                High[0].ToString("G17", CultureInfo.InvariantCulture),
                Low[0].ToString("G17", CultureInfo.InvariantCulture),
                Close[0].ToString("G17", CultureInfo.InvariantCulture),
                Volume[0].ToString(CultureInfo.InvariantCulture)
            });
        }

        private void WriteExportIfReady()
        {
            foreach (DateTime expectedDate in ExpectedDates())
            {
                if (!rowsByTradeDate.ContainsKey(expectedDate))
                    throw new InvalidOperationException("Carver MES tiny export blocked: missing completed daily bar for " + FormatDate(expectedDate) + ".");
            }

            if (rowsByTradeDate.Count != 5)
                throw new InvalidOperationException("Carver MES tiny export blocked: expected exactly five completed daily bars.");

            Directory.CreateDirectory(LockedOutputDirectory);
            string outputPath = Path.Combine(LockedOutputDirectory, LockedOutputFileName);
            string tempPath = outputPath + ".tmp";
            if (File.Exists(outputPath) && !AllowReplaceExistingFile)
                throw new InvalidOperationException("Carver MES tiny export blocked: target file already exists and replacement is disabled.");
            if (File.Exists(tempPath))
                File.Delete(tempPath);

            string header = "provider_symbol,local_contract,timestamp_utc,open,high,low,close,volume";
            File.WriteAllLines(tempPath, new[] { header }.Concat(rowsByTradeDate.Values));
            if (File.Exists(outputPath))
                File.Delete(outputPath);
            File.Move(tempPath, outputPath);
            wroteFile = true;
            Print("CARVER_MES_TINY_DAILY_EXPORT_WRITTEN " + outputPath);
        }

        private static IEnumerable<DateTime> ExpectedDates()
        {
            for (DateTime current = LockedStartDate; current <= LockedEndDate; current = current.AddDays(1))
                yield return current;
        }

        private static string FormatDate(DateTime value)
        {
            return value.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);
        }

        private static string FormatTemplateSessionEndUtc(DateTime tradingDay)
        {
            TimeZoneInfo templateTimeZone = TimeZoneInfo.FindSystemTimeZoneById(LockedTemplateTimeZoneId);
            DateTime localSessionEnd = DateTime.SpecifyKind(
                new DateTime(tradingDay.Year, tradingDay.Month, tradingDay.Day, 16, 0, 0),
                DateTimeKind.Unspecified);
            DateTime utcSessionEnd = TimeZoneInfo.ConvertTimeToUtc(localSessionEnd, templateTimeZone);
            return utcSessionEnd.ToString("yyyy-MM-dd'T'HH:mm:ss'Z'", CultureInfo.InvariantCulture);
        }
    }
}
