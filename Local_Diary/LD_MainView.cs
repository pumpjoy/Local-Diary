using Avalonia;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace Local_Diary;

public class LdMainView : ContentControl
{
    public static readonly StyledProperty<DateTime> ViewDateProperty = AvaloniaProperty.Register<LdMainView, DateTime>(nameof(ViewDate), DateTime.Now);
    
    public static readonly StyledProperty<ViewType> ViewTypeProperty = AvaloniaProperty.Register<LdMainView, ViewType>(nameof(ViewType));
    public static readonly StyledProperty<IEnumerable<DailyEntry>> DateDailyEntriesProperty = AvaloniaProperty.Register<LdMainView, IEnumerable<DailyEntry>>(nameof(DateDailyEntries), new List<DailyEntry>());
    
    
    public DateTime ViewDate
    {
        get => GetValue(ViewDateProperty);
        set => SetValue(ViewDateProperty, value);
    }
    public IEnumerable<DailyEntry> DateDailyEntries
    {
        get => GetValue(DateDailyEntriesProperty);
        set => SetValue(DateDailyEntriesProperty, value);
    }
    public ViewType ViewType
    {
        get => GetValue(ViewTypeProperty);
        set => SetValue(ViewTypeProperty, value);
    }


    private ILdMainView GetView()
    {
        return new MonthView(ViewDate, DateDailyEntries);
    }
    
    
    internal void ForceRender()
    {
        Content = GetView();
    }
}

internal interface ILdMainView
{
    public DateTime ViewDate { get; }
    public IEnumerable<DailyEntry> DateDailyEntries { get; set; }
}

public enum ViewType
{
    Day,
    Week,
    Month,
    Year
}