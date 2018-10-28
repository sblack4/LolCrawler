
-- get vals
SELECT 
	P.summonerName, 
	PF.timestamp, 
	PR.teamId, 
	TS.win, 
	PF.x, PF.y, 
	PF.currentGold, 
	PF.totalGold, 
	PF.minionsKilled, 
	PF.xp
FROM MatchDto M
	LEFT OUTER JOIN PlayerDto P ON M.gameId = P.gameId
	LEFT OUTER JOIN ParticipantFrame PF ON M.gameId = PF.gameId 
		AND P.participantId = PF.participantId
	LEFT OUTER JOIN ParticipantDto PR ON M.gameId = PR.gameId
		AND PR.participantId = P.participantId
	LEFT OUTER JOIN TeamStatsDto TS ON M.gameId = TS.gameId 
		AND PR.teamId = TS.teamId
WHERE M.gameId = 2761581064
ORDER BY PF.timestamp, PF.participantId ASC 