import pyautogui
from datetime import datetime
import psutil
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, Tool
import keyboard
import requests
from bs4 import BeautifulSoup

# ------------------------
# Yerli LLM (Ollama)
# ------------------------
llm = OllamaLLM(model="gemma3:4b")

# ------------------------
# 1. Alət: Chat
# ------------------------
def chat_with_agent(_):
    return f"Chat ilə suallara cevab verin."

chat_tool = Tool(
    name="Chat",
    func=chat_with_agent,
    description="Chat ilə suallara cevab verin."
)

# ------------------------
# 2. Alət: Saat
# ------------------------
def get_time(_):
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

time_tool = Tool(
    name="Saat",
    func=get_time,
    description="Kompüterin cari tarix və saatını göstərir. Nümunə: 'Saat neçedir?', 'Tarix nədir?'."
)

# ------------------------
# 3. Alət: Sistem Vəziyyəti
# ------------------------
def get_system_status(_):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    return f"CPU istifadəsi: {cpu}%, RAM istifadəsi: {ram_usage}%, Disk istifadəsi: {disk_usage}%"

system_tool = Tool(
    name="Sistem Vəziyyəti",
    func=get_system_status,
    description="Kompüterin CPU, RAM və disk istifadəsini göstərir. Nümunə: 'Sistem vəziyyəti nədir?', 'CPU və RAM istifadəsi'."
)

# ------------------------
# 4. Alət: Musiqi Nəzarəti
# ------------------------
def music_control(action):
    action = action.lower()
    if "çal" in action or "play" in action:
        pyautogui.press("playpause")
        return "Musiqi oynadıldı/durduruldu."
    elif "durdur" in action or "pause" in action:
        pyautogui.press("playpause")
        return "Musiqi dayandırıldı/oynadıldı."
    elif "ileri" in action or "next" in action:
        pyautogui.press("nexttrack")
        return "Növbəti mahnı çalınır."
    elif "geri" in action or "prev" in action:
        pyautogui.press("prevtrack")
        return "Əvvəlki mahnı çalınır."
    else:
        return "Müvafiq musiqi əmri tapılmadı."

music_tool = Tool(
    name="Musiqi Nəzarəti",
    func=music_control,
    description="Musiqi pleyeri idarə edir. Əmrlər: 'çal', 'durdur', 'ileri', 'geri'."
)

# ------------------------
# 5. Alət: Mətn Yazmaq
# ------------------------
def type_text(text):
    if not text:
        return "Yazılacaq mətn daxil edilməyib."
    try:
        keyboard.write(text, delay=0.05)
        return f"Mətn yazıldı: {text}"
    except Exception as e:
        return f"Mətn yazıla bilmədi: {str(e)}"

typing_tool = Tool(
    name="Mətn Yazmaq",
    func=type_text,
    description="İstifadəçi tərəfindən verilən mətni yazmaq üçün istifadə olunur. Nümunə: 'yaz salam dünya'."
)

# ------------------------
# 6. Alət: Düyməyə Basmaq (pyautogui ilə)
# ------------------------
def press_key(key_command):
    key_command = key_command.lower().strip()
    if not key_command:
        return "Hansı düyməyə basılacağını göstərmədiniz."
    try:
        pyautogui.press(key_command)
        return f"'{key_command}' düyməsinə basıldı."
    except Exception as e:
        return f"Düyməyə basıla bilmədi: {str(e)}"

press_key_tool = Tool(
    name="Düyməyə Basmaq",
    func=press_key,
    description="Verilən düyməyə basır. Nümunə: 'Enter düyməsinə bas' 'enter', 'tab düyməsinə bas' 'tab', 'Win düyməsinə bas' 'win'."
)


# ------------------------
# 7. Alət: DuckDuckGo Axtarış
# ------------------------
def search_tool_func(query):
    if not query:
        return "Axtarış üçün sorğu daxil edilməyib."
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(f"https://duckduckgo.com/html/?q={query}", headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # DuckDuckGo nəticələri a.result__a içindədir
        for link_tag in soup.select("a.result__a")[:3]:  # İlk 3 nəticə
            title = link_tag.get_text(strip=True)
            link = link_tag['href']
            results.append(f"{title} - {link}")

        return "\n".join(results) if results else "Nəticə tapılmadı."
    except Exception as e:
        return f"Axtarış zamanı xəta baş verdi: {str(e)}"

search_tool = Tool(
    name="Axtarış",
    func=search_tool_func,
    description="İnternetdə DuckDuckGo vasitəsilə məlumat axtarır. Nümunə: 'Python haqqında məlumat axtar'."
)

# ------------------------
#  Sistem promptu
# ------------------------
system_prompt = (
    "Sən köməkçi AI-sən. İstifadəçinin sorğularını analiz et və "
    "lazım olan alətləri sırayla çağır. "
    "Məsələn, istifadəçi 'Saat və sistem vəziyyəti' desə əvvəl 'Saat', sonra 'Sistem Vəziyyəti' alətini çağır. "
    "Musiqi ilə bağlı əmrlər üçün 'Musiqi Nəzarəti' alətini, "
    "düyməyə basma əmrləri üçün 'Düyməyə Basmaq' alətini istifadə et, "
    "sistem vəziyyəti üçün 'Sistem Vəziyyəti', alətini istifadə et, "
    "mətni yazmaq üçün 'Mətn Yazmaq' alətini istifadə et, "
    "Chat ilə suallara cevab verinmək üçün 'Chat' alətini istifadə et, "
    "DuckDuckGo axtarışını etmək üçün 'Axtarış' alətini istifadə et, "
    "Nəticələri istifadəçiyə aydın və başa düşülən şəkildə təqdim et."
)

# ------------------------
#  Agent yaratmaq
# ------------------------
agent = initialize_agent(
    tools=[time_tool, system_tool, music_tool, typing_tool, press_key_tool, chat_tool, search_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    system_message=system_prompt
)

# ------------------------
#  Chat dövrü
# ------------------------
chat_history = []

while True:
    user_input = input("Sualınızı yazın (çıxmaq üçün 'çıkış'): ")
    if user_input.lower() in ["çıkış", "exit", "quit"]:
        print("Söhbət dayandırıldı.")
        break

    # ⚡ LangChain 1.0 uyumlu: invoke() istifadə olunur
    cevap = agent.invoke({"input": user_input})
    
    # Cevabı dict içərisində gəldiyini düşünərək çıxarırıq
    agent_output = cevap.get('output', str(cevap))
    
    chat_history.append((user_input, agent_output))
    
    print("Agentin cavabı:", agent_output)
