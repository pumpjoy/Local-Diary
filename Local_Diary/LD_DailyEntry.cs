using System;

namespace Local_Diary;

/// <summary>
/// Class model for daily entries
/// </summary>
public class DailyEntry
{
    public required DateTime Date { get; set; }
    
    public required string Title { get; set; }
    public required string Content { get; set; }
}