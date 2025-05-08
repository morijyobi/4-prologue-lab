import csv
import os
import random
from main import DATA_FOLDER, weather_options, activity_options, omikuji_themes
import unittest

TEST_DATE = "2025_05_27"
TEST_TXT_PATH = os.path.join(DATA_FOLDER, f"{TEST_DATE}.txt")
TEST_CSV_PATH = os.path.join(DATA_FOLDER, "diary.csv")

class Test_All(unittest.TestCase):
    
    def test_save_data(self):
        weather = "雨"
        activity = "出社"
        satisfaction = 25
        diary_text = "今日は良い日"
        omikuji_text = "おみくじ: テストテーマ"
        weather_index = weather_options.index(weather)
        activity_index = activity_options.index(activity)

      
        rows = []
        if os.path.exists(TEST_CSV_PATH):
            with open(TEST_CSV_PATH, "r", encoding="utf-8-sig") as f:
                rows = [row for row in csv.reader(f) if row[0] != TEST_DATE]

        rows.append([TEST_DATE, weather_index, satisfaction, activity_index])
        with open(TEST_CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

      
        with open(TEST_TXT_PATH, "w", encoding="utf-8") as f:
            f.write(f"[おみくじ]\n{omikuji_text}\n\n")
            f.write("[日記]\n")
            f.write(diary_text)

        
        self.assertTrue(os.path.exists(TEST_TXT_PATH))
        with open(TEST_TXT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("良い日", content)
            self.assertIn("おみくじ", content)


        with open(TEST_CSV_PATH, "r", encoding="utf-8-sig") as f:
            reader = list(csv.reader(f))
            found = [row for row in reader if row[0] == TEST_DATE]
            self.assertEqual(len(found), 1)
            self.assertEqual(int(found[0][1]), weather_index)
            self.assertEqual(int(found[0][2]), satisfaction)  
            self.assertEqual(int(found[0][3]), activity_index)

    def test_omikuji_themes_random(self):
        selected = [random.choice(omikuji_themes) for _ in range(100)]
        self.assertTrue(all([s in omikuji_themes for s in selected]))
        self.assertGreater(len(set(selected)), 1)

if __name__ == "__main__":
    unittest.main()
