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