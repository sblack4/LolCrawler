CREATE TABLE ParticipantIdentityDto (
    MatchDto, player, participantId)
CREATE TABLE TeamBansDto ( MatchDto, TeamStatsDto, pickTurn, championId)
CREATE TABLE TeamStatsDto ( MatchDto, firstDragon, firstInhibitor, bans, baronKills, firstRiftHerald, firstBaron, riftHeraldKills, firstBlood, teamId, firstTower, vilemawKills, inhibitorKills, towerKills, dominionVictoryScore, win, dragonKills)
CREATE TABLE RuneDto ( MatchDto, ParticipantDto, runeId, rank)
CREATE TABLE MasteryDto ( MatchDto, ParticipantDto, masteryId, rank)
CREATE TABLE ParticipantDto ( MatchDto, stats, participantId, runes, timeline, teamId, spell2Id, masteries, highestAchievedSeasonTier, spell1Id, championId)
CREATE TABLE MatchDto ( seasonId, queueId, gameId, participantIdentities, gameVersion, platformId, gameMode, mapId, gameType, teams, participants, gameDuration, gameCreation)


