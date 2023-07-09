SELECT count(dialogue_audio_name) from dialogue;

SELECT DISTINCT count(dialogue_audio_name) from dialogue;

SELECT * from dialogue where dialogue_quest_id = (select quest_id from quest where chapter_id = 26) ORDER BY dialogue_id AESC;

SELECT * from quest WHERE chapter_id = 61;


SELECT DISTINCT * from chapter;

SELECT count(*) from dialogue;


SELECT DISTINCT dialogue_text, dialogue_audio_name FROM (SELECT * FROM dialogue WHERE
dialogue_quest_id IN (SELECT quest_id FROM quest where chapter_id = 39) ORDER BY dialogue_id);