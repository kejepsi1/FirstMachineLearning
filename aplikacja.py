import joblib
import pandas as pd

print("--- Uruchamianie Systemu Wyceny Nieruchomości ---")

# 1. Wczytujemy "zamrożony" model z dysku (to trwa ułamek sekundy)
wczytany_model = joblib.load('moj_model_wyceny.pkl')
print("Model wczytany pomyślnie. Czekam na dane klienta...\n")

# 2. Przygotowujemy dane nowego mieszkania (np. wpisane z formularza na stronie)
# UWAGA: Kolumny muszą nazywać się dokładnie tak samo, jak te w zbiorze treningowym!
# Skoro użyliśmy One-Hot Encoding na dzielnicy, "Centrum" zniknęło jako baza,
# a zostały kolumny Obrzeza i Przedmiescia.
dane_z_formularza = pd.DataFrame({
    'Metraz': [60],
    'Pokoje': [3],
    'Wiek': [5],
    'Dzielnica_Obrzeza': [0],      # 0 oznacza "Nie"
    'Dzielnica_Przedmiescia': [1]  # 1 oznacza "Tak" (czyli to są przedmieścia)
    # Gdybyśmy wpisali tu dwa zera (0 i 0), model uznałby, że to Centrum!
})

# 3. Modelu, wyceń to mieszkanie!
wycena = wczytany_model.predict(dane_z_formularza)

print(f"Parametry: 60m2, 3 pokoje, 5-letnie, Przedmieścia")
print(f"=> Szacowana wartość nieruchomości: {wycena[0]:.0f} zł")