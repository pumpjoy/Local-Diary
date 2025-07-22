using System.Collections.Generic;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;

namespace Local_Diary;

internal class MonthView : ContentControl, ILdMainView
{
    private readonly String[] _daysArray = new String[] { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" };
    
    public MonthView(DateTime _dateTime, IEnumerable<DailyEntry> _dateDailyEntries)
    {
        ViewDate = _dateTime;
        DateDailyEntries = _dateDailyEntries;
        try
        {
            Initialize();
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
        }
    }
    
    private void Initialize()
    {
        Grid mainGrid = new() { RowDefinitions = new("Auto,*") };
        
        // Grid for _days, Monday, Tuesday
        Grid dayGrid = new() { ColumnDefinitions = new("*,*,*,*,*,*,*"), Background = Brushes.Transparent };
        Grid.SetRow(dayGrid, 0);
        for (int i=0; i < 7; i++)
        {
            Grid pGrid = new() { Width = 200, Background = Brushes.Transparent };
            pGrid.Children.Add(new TextBlock() { Text = _daysArray[i], TextAlignment = Avalonia.Media.TextAlignment.Center});
            Grid.SetColumn(pGrid, i);
            dayGrid.Children.Add(pGrid);
        }
        mainGrid.Children.Add(dayGrid);
        
        // Generate actual dates
        Grid dateGrid = new() { ColumnDefinitions = new("*,*,*,*,*,*,*"), Background = Brushes.Transparent };
        Grid.SetRow(dateGrid, 1);
        for (int i=0; i<7; i++)
        {
            Grid pGrid = new() { RowDefinitions = new("*,*,*,*,*") };
            pGrid.Classes.Add("avalonia_calendar_view_gridcolumn");
            Grid.SetColumn(pGrid, i);
            PopulateDateContent(pGrid);
            dateGrid.Children.Add(pGrid);
        }
        
        mainGrid.Children.Add(dateGrid);
        Content = mainGrid;
    }
    
    public DateTime ViewDate { get; }
    public IEnumerable<DailyEntry> DateDailyEntries { get; set; } 


    /// <summary>
    /// Populate the grids with actual dates. 
    /// </summary>
    /// <param name="_col"></param>
    private void PopulateDateContent(Grid _col)
    {
        int col = Grid.GetColumn(_col);
        int numberOfRows = ViewDate.Month == 2 && new DateOnly(ViewDate.Year, ViewDate.Month, 1).DayOfWeek == 0 ? 4 : 5;
        for (int row = 0; row < numberOfRows; row++)
        {
            Thickness thickness = new(1, 1, col == 6 ? 1 : 0, row == numberOfRows - 1 ? 1 : 0);
            Border colBorder = new() { BorderBrush = Brushes.Gray, BorderThickness = thickness };
            colBorder.Classes.Add("avalonia_calendar_view_grid cell");
            Grid pWrapperGrid = new();
            Panel p = new() { Background = Brushes.Transparent };
            var squaredate = PopulateDateNumbers(row, col, out bool outOfBounds, out string? direction);
            var textblock = new TextBlock() { Text = squaredate, TextAlignment = Avalonia.Media.TextAlignment.Right, Margin = new(10), FontSize = 20 };
            if (outOfBounds)
            {
                textblock.Foreground = new SolidColorBrush(Colors.Gray);
            }
            p.Children.Add(textblock);
        }
    }

    
    private string PopulateDateNumbers(int row, int col, out bool outOfBounds, out string? direction)
    {
        var month = ViewDate.Month;
        var year = ViewDate.Year;
        int days_in_month = DateTime.DaysInMonth(year, month);
        var firstDay = (int)new DateTime(year, month, 1).DayOfWeek;
        var lastDay = (int)new DateTime(year, month, days_in_month).DayOfWeek;
        
        // Out of bounds, previous month
        if (row == 0 && col < firstDay)
        {
            var newdate = ViewDate.AddMonths(-1);
            days_in_month = DateTime.DaysInMonth(newdate.Year, newdate.Month);
            outOfBounds = true;
            direction = "prev";
            return (days_in_month - (firstDay - col) + 1).ToString();
        }
        
        // Out of bounds, next month
        if (row == 4 && col > lastDay)
        {
            outOfBounds = true;
            direction = "next";
            return (col - lastDay).ToString();
        }
        
        outOfBounds = false;
        direction = null;
        return row == 0 ? ((col - firstDay) + 1).ToString() : ((((row - 1) * 7) + col + (6 - firstDay) + 2).ToString());
    }
}