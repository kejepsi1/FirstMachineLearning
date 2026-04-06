import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. GENERUJEMY DANE (Paliwo dla modeli)
print("Generuję dane...")
np.random.seed(42)
metraz = np.random.randint(30, 150, 1000)
pokoje = np.where(metraz < 50, np.random.randint(1, 3, 1000), np.random.randint(2, 6, 1000))
wiek = np.random.randint(0, 50, 1000)
dzielnica = np.random.choice(['Centrum', 'Przedmiescia', 'Obrzeza'], 1000)

# Tajny wzór na cenę (model go nie zna, musi go odkryć z samych danych!)
# Centrum jest o 50% droższe, Obrzeża są o 20% tańsze
cena_baza = metraz * 10000
mnoznik_dzielnicy = np.where(dzielnica == 'Centrum', 1.5, np.where(dzielnica == 'Przedmiescia', 1.0, 0.8))
cena_prawdziwa = (cena_baza * mnoznik_dzielnicy) - (wiek * 2000)

# Dodajemy losowy "szum" (w rzeczywistości ktoś czasem przepłaci, a ktoś kupi taniej)
cena_finalna = cena_prawdziwa + np.random.randint(-25000, 25000, 1000)

# Zapisujemy do pliku
df = pd.DataFrame({'Metraz': metraz, 'Pokoje': pokoje, 'Wiek': wiek, 'Dzielnica': dzielnica, 'Cena': cena_finalna})
df.to_csv('duze_mieszkania.csv', index=False)

# =====================================================================
# 2. TRENING I TESTOWANIE (Teraz na 1000 wierszy!)

df = pd.get_dummies(df, columns=['Dzielnica'], drop_first=True)
X = df.drop('Cena', axis=1)
y = df['Cena']

# Zostawiamy 200 mieszkań na testy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n--- WYNIKI STARCIA (Zbiór testowy: 200 mieszkań) ---")

# Model 1: Regresja Liniowa
model_lin = LinearRegression()
model_lin.fit(X_train, y_train)
blad_lin = mean_absolute_error(y_test, model_lin.predict(X_test))
print(f"Błąd Regresji Liniowej: {blad_lin:.0f} zł")

# Model 2: Las Losowy (Random Forest)
model_rf = RandomForestRegressor(random_state=42)
model_rf.fit(X_train, y_train)
blad_rf = mean_absolute_error(y_test, model_rf.predict(X_test))
print(f"Błąd Lasu Losowego:     {blad_rf:.0f} zł")

import matplotlib.pyplot as plt

print("\n--- Analiza 'mózgu' Lasu Losowego ---")

# Wyciągamy informacje o ważności cech bezpośrednio z wytrenowanego modelu
waznosc_cech = model_rf.feature_importances_
nazwy_cech = X.columns

# Łączymy je w tabelę, żeby łatwo było je posortować od najważniejszej do najmniej ważnej
df_waznosc = pd.DataFrame({
    'Cecha': nazwy_cech,
    'Waznosc': waznosc_cech
}).sort_values(by='Waznosc', ascending=True) # Sortujemy rosnąco dla ładnego wykresu

# Rysujemy wykres
plt.style.use('ggplot') # Ładniejszy styl wykresu
plt.figure(figsize=(10, 6))
plt.barh(df_waznosc['Cecha'], df_waznosc['Waznosc'], color='#3498db')
plt.title('Na co Las Losowy zwraca największą uwagę przy wycenie?')
plt.xlabel('Poziom ważności (suma wszystkich wynosi 1.0)')
plt.ylabel('Cecha')
plt.tight_layout()

# Pokazujemy okienko z wykresem
plt.show()

joblib.dump(model_rf, 'moj_model_wyceny.pkl')
print("\nSukces: Model został zapisany na dysku jako 'moj_model_wyceny.pkl'!")