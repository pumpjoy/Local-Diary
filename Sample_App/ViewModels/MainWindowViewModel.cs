using Local_Diary;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace Sample_App.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{ 
    [ObservableProperty]
    private DateTime _currentViewDate = DateTime.Now;

    [ObservableProperty]
    private ViewType _currentViewType = ViewType.Month;
    
    [ObservableProperty]
    private ObservableCollection<DailyEntry> _entries = new ObservableCollection<DailyEntry>();
    
    
    public void Today()
    {
        CurrentViewDate = DateTime.Now;
    }
    
    public void NextDate()
    {
        if (CurrentViewType == ViewType.Month)
        {
            CurrentViewDate = CurrentViewDate.AddMonths(1);
        }
        else if (CurrentViewType == ViewType.Week)
        {
            CurrentViewDate = CurrentViewDate.AddDays(7);
        }
        else if (CurrentViewType == ViewType.Day)
        {
            CurrentViewDate = CurrentViewDate.AddDays(1);
        }
    }

    public void PrevDate()
    {
        if (CurrentViewType == ViewType.Month)
        {
            CurrentViewDate = CurrentViewDate.AddMonths(-1);
        }
        else if (CurrentViewType == ViewType.Week)
        {
            CurrentViewDate = CurrentViewDate.AddDays(-7);
        }
        else if (CurrentViewType == ViewType.Day)
        {
            CurrentViewDate = CurrentViewDate.AddDays(-1);
        }
    }
     
    public void Month() => CurrentViewType = ViewType.Month;
}