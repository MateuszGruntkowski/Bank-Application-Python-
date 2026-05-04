# System bankowy

## Zasady Organizacyjne

1. **Technologie:** Backend: Python (`FastAPI`, `SQLite`, `Pytest`). Frontend: React.
    - Kod, nazwy zmiennych, klas, funkcji, messages commitów, komenatrze oraz dokumentacja powinny być w języku angielskim.
    - Wszystkie funkcjonalności powinny być implementowane w oparciu o testy jednostkowe i Object Oriented Programming.
2. **Wykonywanie zadań:** Zadania są opisane w sposób biznesowy, bez wskazania rozwiązania.
  - Konieczna jest komunikacja z innymi osobami w zespole, by ustalić kolejność zadań, a także integrację z istniejącym kodem.
    - Jeżeli ktoś nie mógł być obecny na zajęciach powinien wykonać swoje zadanie przed zakończeniem sprintu.
    - W wypadku braku zaangażowania członka zespołu, porozmawiajmy o tym wspólnie z prowadzącym, by wypracować rozwiązanie.
3. **Architektura:** Zespół powinien zaproponować czytelną strukturę projektu. Kod powinien być rozbity na kilka plików.
    - Każda funkcja/klasa powinna mieć dokumentację (docstring oraz type hints).
    - Kod powinien zawierać testy jednostkowe (zachęcam do Test Driven Development).
4. **System kontroli wersji:** Zespół jest zobligowany korzystać z Gita podczas wytwarzania oprogramowania.
   - Podczas każdego ze sprintów, każdy z Państwa powinien stworzyć conajmniej jedną gałąź feature.
   - Tworzone commity powinny mieć rzetelne messages.
     - Jeden commit per feature to zła praktyka.
   - Wszystkie zmiany trafiają do develop przez **Pull Request**.
   - Każdy merge do develop powinien być wykonany przez osobę inną niż autor, z minimum jedną opinią (review) przed dokonaniem merge.
     - Jeżeli kod nie działa, brakuje testów, dokumentacji, nie powinien zostać scalony.
   - Po zakończeniu sprintu następuje merge do main razem z oznaczeniem tagu wersji.
     - Osoba odpowiedzialna za te działania po każdym sprincie powinna być wyróżniona w opisie zaangażowania.
5. **Dokumentacja README:** Zespół powinien stworzyć plik README w głównym katalogu projektu, który będzie zawierał:
    - Tytuł i krótki opis.
    - Opis zespołu i obowiązków, zaangażowania każdego z członków.
    - Instrukcję instalacji.
    - Kto wykonał jakie zadania w kolejnych sprintach (tabela), wraz z uwagami.
    - Mile widziany jest diagram klas przedstawiający architekturę aplikacji (nie musi to być UML).
6. **Daily:** Po każdym sprincie, działająca aplikacja będzie omawiana na zajęciach.
    - Będzie to czas na zgłoszenie uwag co do pracy zespołu, napotkanych trudności, pytania dotyczące zadań i implementacji.
    - Na ostatnich zajęciach, każdy z Państwa przedstawi wykonane przez niego funkcjonalności (kod, testy, dokumentacja).
    - Podczas podsumowania po każdym sprincie mogą pojawić się dodatkowe zadania zlecone przez prowadzącego, które również powinny znaleźć się w tabeli z odpowiedzialnością.
7. **Wykorzystanie LLM:** Korzystanie z LLM jest dozwolone i wskazane.
    - Ważne jest jednak, by potrafili Państwo samodzielnie wyjaśnić przeznaczenie i działanie każdej z linii kodu, która została dodana do projektu.
    - Korzystając z LLM powinniśmy szczególnie uważać na przestrzeganie zasad KISS oraz DRY, a także tendencję do overengineering'u - nadmiernego komplikowania prostych funkcjonalności.

---

## Instrukcja Techniczna

### 1. Instalacja i Konfiguracja
Przed pierwszym uruchomieniem projektu należy ręcznie przygotować środowisko:

**Backend:**
1. Przejdź do katalogu `backend/`.
2. Stwórz środowisko wirtualne: `python -m venv .venv`.
3. Aktywuj środowisko:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Zainstaluj biblioteki: `pip install -r requirements.txt`.

**Frontend:**
1. Przejdź do katalogu `frontend/`.
2. Zainstaluj pakiety: `npm install`.

### 2. Uruchamianie Projektu
Po poprawnym zainstalowaniu zależności, możesz korzystać ze skryptów ułatwiających start:
- **Windows:** Uruchom `start.bat`.
- **macOS/Linux:** Uruchom `bash start.sh`.

Skrypty te sprawdzają obecność Node.js i Pythona, a następnie uruchamiają oba serwery w osobnych procesach.

### 3. Personalizacja Banku (Branding)
Każdy zespół powinien nadać swojemu bankowi unikalną nazwę:
- Otwórz plik `frontend/src/config.js`.
- Edytuj pola `bankName`, `bankTagline` oraz `teamName`. Zmiany pojawią się automatycznie w całej aplikacji.

### 4. Architektura i Workflow

- **`backend/services/`**: Katalog na implementację logiki biznesowej (klasy i metody).
  - Większość implementacji powinna znaleźć się w tym katalogu, ale pewne zadania mogą wymagać drobnych zmian w istniejącym kodzie aplikacji.
- **`backend/tests/`**: Testy jednostkowe do Państwa serwisów.
- **`backend/routers/`**: Gotowe endpointy API. Obecnie zwracają one błąd `501 Not Implemented`. Państwa zadaniem jest zmodyfikować je tak, aby wywoływały metody z Waszych serwisów.
- **`backend/models/`**: Definicje tabel bazy danych (`SQLModel`).
