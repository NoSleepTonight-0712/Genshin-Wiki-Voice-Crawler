SELECT count(dialogue_audio_name) from dialogue;

SELECT DISTINCT count(dialogue_audio_name) from dialogue;

SELECT * from dialogue where dialogue_quest_id IN (SELECT quest_id FROM quest where chapter_id = 99);

SELECT * from quest WHERE chapter_id = 124;

SELECT DISTINCT * from chapter;