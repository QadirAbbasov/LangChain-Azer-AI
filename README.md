# Azer AI - Lokal Süni Zəka Köməkçisi

**Azer AI**, **LangChain** kitabxanası və lokal LLM (Ollama) istifadə edərək kompüterinizdə müxtəlif vəzifələri yerinə yetirə bilən interaktiv süni zəka köməkçisidir. Bu layihə sayəsində sistem vəziyyətini yoxlaya, musiqi çalaya, mətn yaza və düymələrə avtomatik basa bilərsiniz. Bütün əmrlər və cavablar **Azericedir**.

---

## Xüsusiyyətlər

- **LangChain ilə İnkişaf etdirilmiş**  
  - Agent dizaynı **LangChain agentləri** üzərində qurulub.  
  - `zero-shot-react-description` agent tipi istifadə olunur, bu da doğru aləti seçməyə imkan verir.  
  - Agent müxtəlif alətləri (tools) analiz edib, sırayla çağırır.

- **Lokal LLM (Ollama) ilə işləyir**  
  - Model: `gemma3:4b`  
  - İnternet bağlantısı tələb etmir, tamamilə lokal işləyir.  

- **Alətlər (Tools)**
  1. **Saat**: Kompüterin cari tarix və saatını göstərir.  
     - Nümunə: `"Saat neçedir?"`, `"Tarix nədir?"`  
  2. **Sistem Vəziyyəti**: CPU, RAM və disk istifadəsini göstərir.  
     - Nümunə: `"Sistem vəziyyəti nədir?"`, `"CPU və RAM istifadəsi"`  
  3. **Musiqi Nəzarəti**: PyAutoGUI vasitəsilə musiqi pleyerini idarə edir.  
     - Əmrlər: `"musiqini çal"`, `"durdur"`, `"ileri"`, `"geri"`  
  4. **Mətn Yazmaq**: Klaviatura vasitəsilə mətn yazır.  
     - Nümunə: `"yaz salam dünya"`  
  5. **Düyməyə Basmaq**: PyAutoGUI vasitəsilə seçilmiş düyməyə basır.  
     - Nümunə: `"Enter düyməsinə bas"`, `"tab düyməsinə bas"`  

- **İnteraktiv Chat Dövrü**  
  - İstifadəçi sorğu verir və LangChain agenti uyğun alətləri seçərək cavab verir.  
  - Çıxmaq üçün `"çıkış"`, `"exit"` və ya `"quit"` yazmaq kifayətdir.

- **Tam Azerice dəstək**  
  - Bütün əmrlər, cavablar və mesajlar Azericedir.  

---

## Quraşdırma

1. **Python 3.10+** quraşdırın.  
2. Lazımi paketləri yükləyin:
```bash
pip install pyautogui keyboard psutil langchain langchain_community
