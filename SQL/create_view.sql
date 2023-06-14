-- only event view
CREATE VIEW dialogue_only_events AS
SELECT *
FROM dialogue
WHERE dialogue_quest_id IN (
        SELECT quest_id
        FROM quest
        where chapter_id IN (
                SELECT chapter_id FROM chapter WHERE chapter_type_id <> 6
            )
    );

DROP VIEW dialogue_only_events;