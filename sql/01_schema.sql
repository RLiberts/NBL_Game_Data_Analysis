USE NBL;
GO

IF OBJECT_ID(N'dbo.Seasons', N'U') IS NULL
CREATE TABLE dbo.Seasons (
    SeasonId UNIQUEIDENTIFIER NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_Seasons PRIMARY KEY (SeasonId)
);
GO

IF OBJECT_ID(N'dbo.Teams', N'U') IS NULL
CREATE TABLE dbo.Teams (
    TeamId UNIQUEIDENTIFIER NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    Code NVARCHAR(10) NULL,
    CONSTRAINT PK_Teams PRIMARY KEY (TeamId)
);
GO

IF OBJECT_ID(N'dbo.Venues', N'U') IS NULL
CREATE TABLE dbo.Venues (
    VenueId UNIQUEIDENTIFIER NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_Venues PRIMARY KEY (VenueId)
);
GO

IF OBJECT_ID(N'dbo.Players', N'U') IS NULL
CREATE TABLE dbo.Players (
    PlayerId UNIQUEIDENTIFIER NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_Players PRIMARY KEY (PlayerId)
);
GO

IF OBJECT_ID(N'dbo.Games', N'U') IS NULL
CREATE TABLE dbo.Games (
    GameId UNIQUEIDENTIFIER NOT NULL,
    SeasonId UNIQUEIDENTIFIER NOT NULL,
    VenueId UNIQUEIDENTIFIER NULL,
    StartTimeLocal DATETIME2(0) NOT NULL,
    StartTimeUtc DATETIME2(0) NOT NULL,
    Status NVARCHAR(20) NOT NULL,
    GameType NVARCHAR(20) NOT NULL,
    Attendance INT NULL,
    CONSTRAINT PK_Games PRIMARY KEY (GameId),
    CONSTRAINT FK_Games_Seasons FOREIGN KEY (SeasonId) REFERENCES dbo.Seasons (SeasonId),
    CONSTRAINT FK_Games_Venues FOREIGN KEY (VenueId) REFERENCES dbo.Venues (VenueId),
    CONSTRAINT CK_Games_Attendance CHECK (Attendance >= 0)
);
GO

IF OBJECT_ID(N'dbo.GameTeams', N'U') IS NULL
CREATE TABLE dbo.GameTeams (
    GameId UNIQUEIDENTIFIER NOT NULL,
    TeamId UNIQUEIDENTIFIER NOT NULL,
    IsHome BIT NOT NULL,
    Score INT NULL,
    TeamReboundsOffensive INT NULL,
    TeamReboundsDefensive INT NULL,
    TeamTurnovers INT NULL,
    TeamFouls INT NULL,
    BiggestLead INT NULL,
    TimeInLeadSeconds INT NULL,
    LeadChanges INT NULL,
    PointsInPaint INT NULL,
    PointsFromBench INT NULL,
    CONSTRAINT PK_GameTeams PRIMARY KEY (GameId, TeamId),
    CONSTRAINT FK_GameTeams_Games FOREIGN KEY (GameId) REFERENCES dbo.Games (GameId),
    CONSTRAINT FK_GameTeams_Teams FOREIGN KEY (TeamId) REFERENCES dbo.Teams (TeamId),
    CONSTRAINT UQ_GameTeams_Home UNIQUE (GameId, IsHome),
    CONSTRAINT CK_GameTeams_Score CHECK (Score >= 0)
);
GO

IF OBJECT_ID(N'dbo.PlayerGameStats', N'U') IS NULL
CREATE TABLE dbo.PlayerGameStats (
    GameId UNIQUEIDENTIFIER NOT NULL,
    PlayerId UNIQUEIDENTIFIER NOT NULL,
    TeamId UNIQUEIDENTIFIER NOT NULL,
    Bib NVARCHAR(4) NULL,
    Position NVARCHAR(5) NULL,
    IsStarter BIT NOT NULL,
    Participated BIT NOT NULL,
    Seconds INT NULL,
    Points INT NULL,
    TwoPtMade INT NULL,
    TwoPtAttempted INT NULL,
    ThreePtMade INT NULL,
    ThreePtAttempted INT NULL,
    FreeThrowsMade INT NULL,
    FreeThrowsAttempted INT NULL,
    ReboundsOffensive INT NULL,
    ReboundsDefensive INT NULL,
    Assists INT NULL,
    Turnovers INT NULL,
    Steals INT NULL,
    Blocks INT NULL,
    Fouls INT NULL,
    PlusMinus INT NULL,
    Efficiency INT NULL,
    CONSTRAINT PK_PlayerGameStats PRIMARY KEY (GameId, PlayerId),
    CONSTRAINT FK_PlayerGameStats_Players FOREIGN KEY (PlayerId) REFERENCES dbo.Players (PlayerId),
    CONSTRAINT FK_PlayerGameStats_GameTeams FOREIGN KEY (GameId, TeamId) REFERENCES dbo.GameTeams (GameId, TeamId),
    CONSTRAINT CK_PlayerGameStats_TwoPt CHECK (TwoPtMade <= TwoPtAttempted),
    CONSTRAINT CK_PlayerGameStats_ThreePt CHECK (ThreePtMade <= ThreePtAttempted),
    CONSTRAINT CK_PlayerGameStats_FT CHECK (FreeThrowsMade <= FreeThrowsAttempted),
    CONSTRAINT CK_PlayerGameStats_NonNegative CHECK (
    Seconds >= 0 AND Points >= 0 AND TwoPtMade >= 0 AND ThreePtMade >= 0
    AND FreeThrowsMade >= 0 AND ReboundsOffensive >= 0 AND ReboundsDefensive >= 0
    AND Assists >= 0 AND Turnovers >= 0 AND Steals >= 0 AND Blocks >= 0 AND Fouls >= 0
    )
);
GO

IF OBJECT_ID(N'dbo.GamePeriodScores', N'U') IS NULL
CREATE TABLE dbo.GamePeriodScores (
    GameId UNIQUEIDENTIFIER NOT NULL,
    TeamId UNIQUEIDENTIFIER NOT NULL,
    PeriodId TINYINT NOT NULL,
    Points INT NOT NULL,
    CONSTRAINT PK_GamePeriodScores PRIMARY KEY (GameId, TeamId, PeriodId),
    CONSTRAINT FK_GamePeriodScores_GameTeams FOREIGN KEY (GameId, TeamId) REFERENCES dbo.GameTeams (GameId, TeamId),
    CONSTRAINT CK_GamePeriodScores_Period CHECK (PeriodId BETWEEN 1 AND 4 OR PeriodId >= 11),
    CONSTRAINT CK_GamePeriodScores_Points CHECK (Points >= 0)
);
GO