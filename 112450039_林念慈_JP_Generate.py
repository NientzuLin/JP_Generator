#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext
import random
from typing import List, Dict, Set
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class PhonologySystem:
    """音韻系統 - 日語風格"""
    consonants: Set[str] = field(default_factory=lambda: {'k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w'})
    vowels: Set[str] = field(default_factory=lambda: {'a', 'i', 'u', 'e', 'o'})
    n_end: List[str] = field(default_factory=lambda: ['n', ''])  # 鼻音結尾
    
    def generate_syllable(self) -> str:
        """生成日語風格音節 (CV 或 CVN)"""
        syllable = random.choice(list(self.consonants)) + random.choice(list(self.vowels))
        if random.random() < 0.3:  # 30% 機率加鼻音
            syllable += random.choice(self.n_end)
        return syllable
    
    def generate_word(self, syllable_count: int = None, word_type: str = "noun") -> str:
        """生成日語風格詞語"""
        if syllable_count is None:
            syllable_count = random.randint(2, 3)
        
        word = ""
        for _ in range(syllable_count):
            word += self.generate_syllable()
        
        # 添加詞尾
        if word_type == "verb":
            word += random.choice(['ru', 'mu', 'su', 'ku', 'ta'])
        elif word_type == "noun":
            word += random.choice(['ko', 'mi', 'ra', 'to', 'na'])
        
        return word

@dataclass
class MorphologyRule:
    """構詞規則"""
    name: str
    rule_type: str  # prefix, suffix
    marker: str
    meaning: str

@dataclass
class MorphologySystem:
    """構詞系統"""
    rules: List[MorphologyRule] = field(default_factory=list)
    
    def add_rule(self, name: str, rule_type: str, marker: str, meaning: str):
        """添加構詞規則"""
        rule = MorphologyRule(name, rule_type, marker, meaning)
        self.rules.append(rule)
    
    def apply_morphology(self, base_word: str, rule_name: str) -> str:
        """應用構詞規則"""
        for rule in self.rules:
            if rule.name == rule_name:
                if rule.rule_type == 'prefix':
                    return rule.marker + base_word
                elif rule.rule_type == 'suffix':
                    return base_word + rule.marker
        return base_word

@dataclass
class SyntaxSystem:
    """句法系統 - 日語 SOV 語序"""
    word_order: str = "SOV"
    particles: Dict[str, List[str]] = field(default_factory=lambda: {
        'subject': ['wa', 'ga'],
        'object': ['wo'],
        'direction': ['e', 'o']
    })
    
    def generate_sentence(self, subject: str, verb: str, obj: str = "", add_adverb: bool = False, adverb: str = "") -> str:
        """根據日語語序生成句子"""
        parts = []
        
        # 主語 + 助詞
        parts.append(subject + random.choice(self.particles['subject']))
        
        # 補語 + 助詞 (如果有)
        if obj:
            parts.append(obj + random.choice(self.particles['object']))
        
        # 副詞 (如果有)
        if add_adverb and adverb:
            parts.append(adverb + random.choice(self.particles['direction']))
        
        # 動詞 (SOV 語序，動詞在最後)
        parts.append(verb)
        
        return ' '.join(parts) + "."

class JapaneseLanguageCreatorUI:
    """日語風格語言創造者 GUI"""
    
    def __init__(self):
        self.phonology = PhonologySystem()
        self.morphology = MorphologySystem()
        self.syntax = SyntaxSystem()
        self.vocabulary = defaultdict(list)
        
        # 初始化構詞規則
        self.init_default_rules()
        
        # 建立 UI
        self.setup_ui()
    
    def init_default_rules(self):
        """初始化預設構詞規則"""
        self.morphology.add_rule("plural", "suffix", "tachi", "複數")
        self.morphology.add_rule("past", "suffix", "ta", "過去式")
        self.morphology.add_rule("negative", "prefix", "fu", "否定")
    
    def setup_ui(self):
        """建立使用者界面"""
        self.window = tk.Tk()
        self.window.title("日語風格語言創造者遊戲 🎌")
        self.window.geometry("800x700")
        self.window.configure(bg='#f0f0f0')
        
        # 標題
        title_frame = tk.Frame(self.window, bg='#4a90e2', height=60)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🌸 日語風格語言創造者 🌸", 
            font=("Arial", 18, "bold"),
            bg='#4a90e2',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # 主要容器
        main_container = tk.Frame(self.window, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 左側：控制面板
        left_panel = tk.LabelFrame(main_container, text="🎮 控制面板", font=("Arial", 12, "bold"), bg='#f0f0f0')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 第一關：音韻系統
        level1_frame = tk.LabelFrame(left_panel, text="第一關：音韻系統 🔤", font=("Arial", 10, "bold"), bg='#ffffff')
        level1_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(level1_frame, text=f"子音: {', '.join(sorted(self.phonology.consonants))}", 
                 wraplength=300, justify='left', bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        tk.Label(level1_frame, text=f"母音: {', '.join(sorted(self.phonology.vowels))}", 
                 bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        
        btn_gen_words = tk.Button(
            level1_frame, 
            text="生成詞語 (5個)", 
            command=self.generate_vocabulary,
            bg='#5cb85c',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        )
        btn_gen_words.pack(pady=5)
        
        # 第二關：構詞系統
        level2_frame = tk.LabelFrame(left_panel, text="第二關：構詞系統 🔧", font=("Arial", 10, "bold"), bg='#ffffff')
        level2_frame.pack(fill='x', padx=10, pady=5)
        
        rules_text = "規則:\n"
        for rule in self.morphology.rules:
            rules_text += f"• {rule.meaning}: {rule.marker} ({rule.rule_type})\n"
        
        tk.Label(level2_frame, text=rules_text, justify='left', bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        
        btn_show_morphology = tk.Button(
            level2_frame, 
            text="展示構詞變化", 
            command=self.show_morphology,
            bg='#5cb85c',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        )
        btn_show_morphology.pack(pady=5)
        
        # 第三關：句法系統
        level3_frame = tk.LabelFrame(left_panel, text="第三關：句法系統 📝", font=("Arial", 10, "bold"), bg='#ffffff')
        level3_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(level3_frame, text=f"語序: {self.syntax.word_order} (主語-賓語-動詞)", 
                 bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        tk.Label(level3_frame, text=f"助詞: は/が (主格), を (受格)", 
                 bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        
        sentence_control_frame = tk.Frame(level3_frame, bg='#ffffff')
        sentence_control_frame.pack(pady=5)
        
        btn_gen_1 = tk.Button(
            sentence_control_frame, 
            text="生成 1 句", 
            command=lambda: self.generate_sentences(1),
            bg='#0275d8',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        )
        btn_gen_1.pack(side='left', padx=5)
        
        btn_gen_5 = tk.Button(
            sentence_control_frame, 
            text="生成 5 句", 
            command=lambda: self.generate_sentences(5),
            bg='#0275d8',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        )
        btn_gen_5.pack(side='left', padx=5)
        
        # 右側：輸出面板
        right_panel = tk.LabelFrame(main_container, text="📋 輸出結果", font=("Arial", 12, "bold"), bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            right_panel, 
            wrap=tk.WORD, 
            font=("Courier New", 11),
            bg='#ffffff',
            height=30
        )
        self.output_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 底部按鈕
        bottom_frame = tk.Frame(self.window, bg='#f0f0f0')
        bottom_frame.pack(fill='x', padx=20, pady=10)
        
        btn_clear = tk.Button(
            bottom_frame, 
            text="清空輸出", 
            command=self.clear_output,
            bg='#d9534f',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        )
        btn_clear.pack(side='left')
        
        btn_showcase = tk.Button(
            bottom_frame, 
            text="🎉 展示完整語言", 
            command=self.final_showcase,
            bg='#f0ad4e',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        )
        btn_showcase.pack(side='right')
        
        # 初始歡迎訊息
        self.show_welcome()
    
    def show_welcome(self):
        """顯示歡迎訊息"""
        welcome = """
╔═══════════════════════════════════════════════════╗
║     🌸 歡迎來到日語風格語言創造者遊戲！ 🌸        ║
╚═══════════════════════════════════════════════════╝

你將通過三個層次來創造一個日語風格的語言：

📍 第一關：音韻系統 (Phonology)
   - 使用日語音節結構 (CV, CVN)
   - 點擊「生成詞語」來創建詞彙

📍 第二關：構詞系統 (Morphology)
   - 應用日語構詞規則
   - 查看複數、過去式、否定等變化

📍 第三關：句法系統 (Syntax)
   - 使用 SOV 語序 (日語語序)
   - 生成完整的句子

開始探索吧！ 🚀
═══════════════════════════════════════════════════

"""
        self.output_text.insert('1.0', welcome)
    
    def clear_output(self):
        """清空輸出"""
        self.output_text.delete('1.0', tk.END)
    
    def append_output(self, text: str):
        """添加輸出文字"""
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
    
    def generate_vocabulary(self):
        """生成詞彙"""
        self.append_output("\n🎲 生成新詞彙：")
        self.append_output("-" * 50)
        
        word_types = [
            ('noun', '名詞'),
            ('verb', '動詞'),
            ('noun', '名詞'),
            ('adjective', '形容詞'),
            ('noun', '名詞')
        ]
        
        for i, (word_type, chinese) in enumerate(word_types, 1):
            word = self.phonology.generate_word(random.randint(2, 3), word_type)
            self.vocabulary[word_type].append(word)
            self.append_output(f"{i}. {word} ({chinese})")
        
        self.append_output(f"\n✅ 已生成 5 個詞語！")
    
    def show_morphology(self):
        """展示構詞變化"""
        self.append_output("\n🔧 構詞變化展示：")
        self.append_output("-" * 50)
        
        if self.vocabulary['noun']:
            noun = random.choice(self.vocabulary['noun'])
            plural = self.morphology.apply_morphology(noun, "plural")
            self.append_output(f"名詞複數: {noun} → {plural}")
        
        if self.vocabulary['verb']:
            verb = random.choice(self.vocabulary['verb'])
            past = self.morphology.apply_morphology(verb, "past")
            self.append_output(f"動詞過去式: {verb} → {past}")
        
        if self.vocabulary.get('adjective'):
            adj = random.choice(self.vocabulary['adjective'])
            neg = self.morphology.apply_morphology(adj, "negative")
            self.append_output(f"形容詞否定: {adj} → {neg}")
    
    def generate_sentences(self, count: int):
        """生成句子"""
        self.append_output(f"\n📝 生成 {count} 個句子：")
        self.append_output("-" * 50)
        
        # 確保有足夠的詞彙
        if not self.vocabulary['noun']:
            for _ in range(3):
                self.vocabulary['noun'].append(self.phonology.generate_word(2, "noun"))
        if not self.vocabulary['verb']:
            for _ in range(2):
                self.vocabulary['verb'].append(self.phonology.generate_word(2, "verb"))
        
        for i in range(count):
            # 隨機選擇句型
            pattern = random.choice([
                ('S', 'O', 'V'),       # 主語 + 賓語 + 動詞
                ('S', 'V'),            # 主語 + 動詞
                ('S', 'O', 'V', 'Adv') # 主語 + 賓語 + 動詞 + 副詞
            ])
            
            subject = random.choice(self.vocabulary['noun'])
            verb = random.choice(self.vocabulary['verb'])
            obj = random.choice(self.vocabulary['noun']) if 'O' in pattern else ""
            
            add_adverb = 'Adv' in pattern
            adverb = self.phonology.generate_word(2, "noun") if add_adverb else ""
            
            sentence = self.syntax.generate_sentence(subject, verb, obj, add_adverb, adverb)
            self.append_output(f"{i+1}. {sentence}")
    
    def final_showcase(self):
        """最終語言展示"""
        self.append_output("\n" + "=" * 50)
        self.append_output("🎉 你創造的日語風格語言展示 🎉")
        self.append_output("=" * 50)
        
        self.append_output("\n🔤 音韻系統:")
        self.append_output(f"   子音: {', '.join(sorted(self.phonology.consonants))}")
        self.append_output(f"   母音: {', '.join(sorted(self.phonology.vowels))}")
        self.append_output(f"   音節結構: CV, CVN (鼻音結尾)")
        
        self.append_output("\n🔧 構詞系統:")
        for rule in self.morphology.rules:
            self.append_output(f"   • {rule.meaning}: {rule.marker} ({rule.rule_type})")
        
        self.append_output("\n📝 句法系統:")
        self.append_output(f"   基本語序: {self.syntax.word_order} (主語-賓語-動詞)")
        self.append_output(f"   助詞系統: は/が (主格), を (受格), へ/を (方向)")
        
        self.append_output("\n📚 詞彙統計:")
        for word_class, words in self.vocabulary.items():
            if words:
                self.append_output(f"   {word_class}: {len(words)} 個")
        
        self.append_output("\n🌟 範例句子:")
        self.generate_sentences(3)
        
        self.append_output("\n" + "=" * 50)
    
    def run(self):
        """運行程式"""
        self.window.mainloop()

def main():
    """主程式"""
    app = JapaneseLanguageCreatorUI()
    app.run()

if __name__ == "__main__":
    main()