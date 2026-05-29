// Process-only NinjaTrader Desktop export bridge for Carver.
// Import into NinjaTrader 8 only after a separate operator execution gate.
// Attach to a 1 Day ZN 06-26 chart. It writes only completed daily OHLCV rows.

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
    public class CarverDailyBarExporter : Indicator
    {
        private readonly List<string> rows = new List<string>();
        private bool wroteFile;
        private DateTime lastCompletedTradeDate;

        [NinjaScriptProperty]
        [Display(Name = "Expected NinjaTrader instrument full name", Order = 1, GroupName = "Carver")]
        public string ExpectedNinjaTraderInstrumentFullName { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Expected Carver display symbol", Order = 2, GroupName = "Carver")]
        public string ExpectedCarverDisplaySymbol { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Expected instrument code", Order = 3, GroupName = "Carver")]
        public string ExpectedInstrumentCode { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Expected contract month", Order = 4, GroupName = "Carver")]
        public string ExpectedContractMonth { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Last completed trade date UTC (yyyy-MM-dd)", Order = 5, GroupName = "Carver")]
        public string LastCompletedTradeDateUtc { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Required bars", Order = 6, GroupName = "Carver")]
        public int RequiredBars { get; set; }

        [NinjaScriptProperty]
        [Display(Name = "Output directory", Order = 7, GroupName = "Carver")]
        public string OutputDirectory { get; set; }

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Name = "CarverDailyBarExporter";
                Description = "Exports a locked Carver ZN 06-26 daily OHLCV CSV to quarantine.";
                Calculate = Calculate.OnBarClose;
                IsOverlay = true;
                DisplayInDataBox = false;
                DrawOnPricePanel = false;
                IsSuspendedWhileInactive = false;
                BarsRequiredToPlot = 0;

                ExpectedNinjaTraderInstrumentFullName = "ZN JUN26";
                ExpectedCarverDisplaySymbol = "ZN 06-26";
                ExpectedInstrumentCode = "ZN";
                ExpectedContractMonth = "06-26";
                LastCompletedTradeDateUtc = "2026-05-28";
                RequiredBars = 257;
                OutputDirectory = @"C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\desktop_daily_exports";
            }
            else if (State == State.DataLoaded)
            {
                rows.Clear();
                wroteFile = false;
                ValidateConfiguration();
            }
        }

        protected override void OnBarUpdate()
        {
            if (wroteFile || CurrentBar < 0)
                return;

            DateTime tradeDate = Time[0].Date;
            if (tradeDate > lastCompletedTradeDate)
            {
                WriteExportIfReady();
                return;
            }

            rows.Add(ToCsvRow(tradeDate));
            while (rows.Count > RequiredBars)
                rows.RemoveAt(0);

            if (tradeDate >= lastCompletedTradeDate)
                WriteExportIfReady();
        }

        private void ValidateConfiguration()
        {
            if (Instrument == null || Instrument.FullName != ExpectedNinjaTraderInstrumentFullName)
                throw new InvalidOperationException("Carver export blocked: attach only to ZN JUN26.");

            if (BarsPeriod == null || BarsPeriod.BarsPeriodType != BarsPeriodType.Day || BarsPeriod.Value != 1)
                throw new InvalidOperationException("Carver export blocked: chart must use 1 Day bars.");

            if (ExpectedNinjaTraderInstrumentFullName != "ZN JUN26"
                || ExpectedCarverDisplaySymbol != "ZN 06-26"
                || ExpectedInstrumentCode != "ZN"
                || ExpectedContractMonth != "06-26")
                throw new InvalidOperationException("Carver export blocked: identity fields are locked to ZN 06-26.");

            if (RequiredBars <= 0)
                RequiredBars = 257;

            if (RequiredBars != 257)
                throw new InvalidOperationException("Carver export blocked: RequiredBars is locked to 257.");

            string effectiveLastCompletedTradeDate = string.IsNullOrWhiteSpace(LastCompletedTradeDateUtc)
                ? "2026-05-28"
                : LastCompletedTradeDateUtc;

            if (!DateTime.TryParseExact(
                    effectiveLastCompletedTradeDate,
                    "yyyy-MM-dd",
                    CultureInfo.InvariantCulture,
                    DateTimeStyles.None,
                    out lastCompletedTradeDate))
                throw new InvalidOperationException("Carver export blocked: set LastCompletedTradeDateUtc as yyyy-MM-dd.");

            LastCompletedTradeDateUtc = effectiveLastCompletedTradeDate;

            string lockedRoot = Path.GetFullPath(@"C:\Users\openclaw\Desktop\Carver\data\quarantine\ninjatrader\desktop_daily_exports")
                .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            string requestedRoot = Path.GetFullPath(OutputDirectory ?? string.Empty)
                .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);

            if (!string.Equals(requestedRoot, lockedRoot, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("Carver export blocked: output must stay in the Carver desktop_daily_exports quarantine.");
        }

        private string ToCsvRow(DateTime tradeDate)
        {
            return string.Join(",", new[]
            {
                ExpectedInstrumentCode,
                ExpectedContractMonth,
                ExpectedCarverDisplaySymbol,
                "Last",
                "1 Day",
                tradeDate.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture),
                Open[0].ToString("G17", CultureInfo.InvariantCulture),
                High[0].ToString("G17", CultureInfo.InvariantCulture),
                Low[0].ToString("G17", CultureInfo.InvariantCulture),
                Close[0].ToString("G17", CultureInfo.InvariantCulture),
                Volume[0].ToString("G17", CultureInfo.InvariantCulture)
            });
        }

        private void WriteExportIfReady()
        {
            if (rows.Count < RequiredBars)
            {
                Print("CARVER_NINJATRADER_DESKTOP_DAILY_EXPORT_WAITING rows=" + rows.Count.ToString(CultureInfo.InvariantCulture)
                    + " required=" + RequiredBars.ToString(CultureInfo.InvariantCulture));
                throw new InvalidOperationException("Carver export blocked: fewer than 257 completed daily rows are loaded.");
            }

            Directory.CreateDirectory(OutputDirectory);
            string outputPath = Path.Combine(OutputDirectory, "ZN_06-26_Daily_Last_257.csv");
            string tempPath = outputPath + ".tmp";
            string header = "instrument,contract_month,display_symbol,bar_type,timeframe,trade_date,open,high,low,close,volume";
            IEnumerable<string> finalRows = rows.Skip(rows.Count - RequiredBars);
            if (File.Exists(tempPath))
                File.Delete(tempPath);
            File.WriteAllLines(tempPath, new[] { header }.Concat(finalRows));
            if (File.Exists(outputPath))
                File.Delete(outputPath);
            File.Move(tempPath, outputPath);
            wroteFile = true;
            Print("CARVER_NINJATRADER_DESKTOP_DAILY_EXPORT_WRITTEN " + outputPath);
        }
    }
}
