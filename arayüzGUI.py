from tkinter import *
import tkinter as tk


class Node:
    def __init__(self, data):
        self.data = data   #Düğümün verisini saklar
        self.next = None    #Bir sonraki düğüme işaret eder
        

class LinkedList:
    def __init__(self):
        self.head = None   
        
#likend liste ekleme yapıyoruz 
    def append(self, data):
        new_node = Node(data)
        if self.head is None:             # Eğer listee boşsa yeni düğümü baş olarak atar
            self.head = new_node
            return
        last_node = self.head     #Eğer liste boş değilse son düğümü bulana kadar ilerler
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node   #Son düğümün next özelliğini yeni düğüme atar

#linked listen çıkarım yapmak
    def remove(self, data):
        cur_node = self.head
        if cur_node and cur_node.data == data:     #Eğer başlangıç düğümü çıkarılacak düğüm ise, baş düğümü bir sonraki düğüme atar
            self.head = cur_node.next
            cur_node = None
            return
        prev = None                  #Önceki düğümü saklar
       
        while cur_node and cur_node.data != data:    #Çıkarılacak düğüm bulunana kadar listeyi döngü içinde gezer
            prev = cur_node
            cur_node = cur_node.next
        if cur_node is None:
            return
        prev.next = cur_node.next          #Çıkarılacak düğümün önceki düğümünün next özelliğini, çıkarılacak düğümün bir sonraki düğümüne atar
        cur_node = None

    def print_list(self):
        cur_node = self.head
        while cur_node:
            print(cur_node.data)
            cur_node = cur_node.next

secilen_ürünler = LinkedList()


def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))


#Ana Penceredeki Butonlara tıklandığında çalışacak işlemler burada

def button_click(ürün, button):
    if button['bg'] == 'SystemButtonFace':     #eğer buton rengi şuanki mevcut renk ise çalışacak kod ve yeşil yapar
        button['bg'] = 'green'
        secilen_ürünler.append(ürün)
        print(f"{ürün} butonuna tıklandı ve linked list'e eklendi!")

    else:
        button['bg'] = 'SystemButtonFace'               #buton rengi mevcut rengi olmasığı için çalışır rengini önceki mevcut rengine dönüştürür.
        secilen_ürünler.remove(ürün)
        print(f"{ürün} butonuna tıklandı ve linked list'den çikarildi!")
    secilen_ürünler.print_list()
   
#Bu fonksiyonu tarfileri göste butonunu çağırırken çalıştırıyoruz 
def sonuclari_goster():
    secilen_urunler = []
    current_node = secilen_ürünler.head
    while current_node:     #Linked listeyi döngü içinde gezer ve her düğümün verisini listeye ekler
        secilen_urunler.append(current_node.data)
        current_node = current_node.next

    sonuclar = tarifleri_karsilastir(secilen_urunler)
    # ek pencere açılır 
    yeni_pencere = tk.Toplevel()
    yeni_pencere.geometry("1000x600")
    yeni_pencere.title("Tarifler")

    text = Text(yeni_pencere, font="Tahoma 14")
    text.pack(fill=BOTH, expand=True)

    for tarif_ad, yuzde, eksikler in sonuclar:
        if yuzde == 100:
            result_str = f"{tarif_ad} tarifi ile %100 uyuştunuz. Tüm malzemeler var."
        else:
            eksikler_str = ", ".join(eksikler)
            result_str = f"{tarif_ad} tarifi ile %{yuzde} uyuştunuz. Eksik malzemeler: {eksikler_str}"
        text.insert(END, result_str + "\n")
        #her tarif için buton ekliyoruz
        button = Button(text, text="Nasıl Yapılır?")
        text.window_create(END, window=button)
        text.insert(END, "\n\n")  # Butonlar arasında boşluk bırakın

# Tarif sınıfı
class Tarif:
    def __init__(self, ad, malzemeler):     # Her bir tarif, ad ve malzemelerin bir listesi (malzemeler) ile tanımlanır.
        self.ad = ad
        self.malzemeler = malzemeler

    # TreeNode sınıfı ağaç veri yapısının her bir düğümünü temsil eder
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = {}               #Düğümün çocuklarını saklar

class TarifAgaci:
    def __init__(self):
        self.root = TreeNode(None)       #Ağacın kök düğümünü oluşturur
    
     # Ağaca tarif ekliyoruz
    def tarif_ekle(self, tarif):   
        current_node = self.root         # Başlangıç düğümünü alır.
  
        for malzeme in tarif.malzemeler:                              #Her malzeme için eğer  
            if malzeme not in current_node.children:                  #bu malzeme mevcut düğümün çocukları arasında değilse
                current_node.children[malzeme] = TreeNode(malzeme)    # yeni bir düğüm oluşturur ve bu düğümü mevcut düğümün çocuklarına ekler
            current_node = current_node.children[malzeme]             #mevcut düğümü bir sonraki düğüme taşır
        current_node.data = tarif                                     #tarif nesnesini yaprak düğümde saklar

    def _traverse(self, node):
        if node is not None:
            if node.data is not None:                #Eğer düğümün verisi varsa, bu veriyi döndürür
                yield node.data
            for child in node.children.values():     #düğümün her çocuğu için döngü içinde gezer   
                yield from self._traverse(child)     
    
    #Ağacın kendisini döngü içinde gezer
    def __iter__(self):
        return self._traverse(self.root)
    
    # Ağacın bir sonraki düğümünü döndürür
    def __next__(self):
        while self._stack:
            node = self._stack.pop()               
            if node.children:                                       #eğer düğümün çocukları varsa bu çocukları yığına ekler
                self._stack.extend(node.children.values())
            elif node.data is not None:                             # Eğer düğümün verisi varsa, bu düğümü döndürür
                return node
        raise StopIteration                                         # bir jeneratör fonksiyonunun sona erdiğini belirtmek için kullanılır  yield ifadesinden sonra duraklatılırlar

    

# Kullanım örneği
tarif_agaci = TarifAgaci()

# Tarif eklemek için örnek
tarif_agaci.tarif_ekle(Tarif("Menemen", ["Domates", "Soğan", "Yumurta", "Yeşil Biber"]))
tarif_agaci.tarif_ekle(Tarif("Krep", ["İnek Sütü", "Yumurta", "Un", "Tereyağı", "Kabartma Tozu", "Vanilya"]))
tarif_agaci.tarif_ekle(Tarif("Mercimek Çorbası", ["Mercimek", "Soğan","Havuç",""]))
tarif_agaci.tarif_ekle(Tarif("Fırında Karnabahar Kızartması", ["Karnabahar", "Un", "İnek Sütü", "Yumurta"]))
tarif_agaci.tarif_ekle(Tarif("Mercimek Köftesi", ["Kırmızı Mercimek", "Bulgur", "Soğan", "Salatalık", "Limon", "Pul Biber"]))
tarif_agaci.tarif_ekle(Tarif("Saray Köftesi", ["Kıyma", "Soğan", "Yumurta", "Galeta Unu"]))
tarif_agaci.tarif_ekle(Tarif("Arnavut Ciğeri", ["Dana Ciğer", "Un", "Patates", "Kırmızı Soğan", "Sumak", "Kişniş", "Maydanoz"]))
tarif_agaci.tarif_ekle(Tarif("Frambuazlı Cheescake", ["Yumurta", "Krema", "Labne", "Buğday Nişastası", "Frambuaz", "Vanilya", "Un"]))
tarif_agaci.tarif_ekle(Tarif("Vişne Soslu Yaprak Sarma", ["Vişne", "Asma Yaprağı", "Pirinç", "Soğan", "Nane", "Karabiber", "Kırmızı Tatlı Biber", "Limon"]))
tarif_agaci.tarif_ekle(Tarif("Elmalı Şerit Kurabiye", ["Un", "Buğday Nişastası", "Elma", "Tarçın","Kabartma Tozu","Vanilya","Yumurta","Tereyağ"]))
tarif_agaci.tarif_ekle(Tarif("Patates Tabanlı Pizza", ["İnek Sütü", "Yumurta", "Un", "Tereyağı", "Kabartma Tozu","Patates","Mozzarella Peynir","Sucuk","Yeşil Biber","Kapya Biber","Sarımsak","Domates","Mantar","Mısır"]))
tarif_agaci.tarif_ekle(Tarif("Kıymalı Sebzeli Graten", ["Kıyma", "Soğan","Havuç","Patates","Karabiber","Un","Tereyağı","İnek Sütü","Sarımsak","Yoğurt","Yumurta","Kaşar Peynir"]))
tarif_agaci.tarif_ekle(Tarif(" Dalyan Köfte", ["Kıyma", "Soğan", "Galeta Unu", "Yumurta","Karabiber","Kırmızı Tatlı Biber","Bezelye","Havuç",]))
tarif_agaci.tarif_ekle(Tarif("Ispanak ve Mantarlı Rulo Börek", ["Ispanak", "Mantar", "Soğan", "Yumurta", "Karabiber", "Yufka"]))
tarif_agaci.tarif_ekle(Tarif("Bal Kabağı Risotto", ["Bal Kabağı", "Risotto Pirinci", "Soğan", "Tavuk Suyu", "Parmesan Peyniri","Havuç"]))
tarif_agaci.tarif_ekle(Tarif("Fırında Sebzeli Kuzu Eti", ["Kuzu Eti", "Patates", "Havuç", "Kabak", "Soğan", "Sarımsak","Maydanoz", "Dereotu","Yeşil Biber","Kapya Biber"]))
tarif_agaci.tarif_ekle(Tarif("Sebzeli Karışık Tava", ["Patates", "Soğan", "Yeşil Biber", "Havuç", "Brokoli", "Kabak", "Sarımsak", "Tavuk Göğsü", "Margarin", "Tuz", "Karabiber"]))
tarif_agaci.tarif_ekle(Tarif("Ispanaklı Peynirli Börek", ["Yufka", "Ispanak", "Beyaz Peynir", "Sarımsak", "Tereyağı"]))
tarif_agaci.tarif_ekle(Tarif("Mantarlı Tavuk Sote", ["Tavuk Göğsü", "Mantar", "Soğan", "Yeşil Biber", "Sarımsak", "İnek Sütü", "Un", "Karabiber"]))
tarif_agaci.tarif_ekle(Tarif("Fırında Kabak Mücver", ["Kabak", "Soğan", "Maydanoz", "Yumurta", "Un", "Sarımsak"]))
tarif_agaci.tarif_ekle(Tarif("Domates Salatalık Salsa", ["Domates", "Salatalık", "Soğan", "Yeşil Biber", "Limon", "Nane"]))
tarif_agaci.tarif_ekle(Tarif("Meyve Salatası", ["Elma", "Portakal", "Çilek", "Muz", "Mango", "Limon","Vişne","Kiraz","Erik","Kavun","Hurma"]))
tarif_agaci.tarif_ekle(Tarif("Deniz Mahsulleri Linguine", ["Karides", "Kalamar", "Midye", "Domates", "Sarımsak", "Karabiber"]))
tarif_agaci.tarif_ekle(Tarif("Karnabahar Köftesi", ["Karnabahar", "Soğan", "Sarımsak", "Un", "Yumurta", "Karabiber", "Nane"]))
tarif_agaci.tarif_ekle(Tarif("Muzlu Yoğurtlu Granola", ["Muz", "Yoğurt", "Granola", "Bal", "Badem Sütü"]))



def tarifleri_karsilastir(secilen_urunler):
    sonuclar = []
    for tarif in tarif_agaci:
        if not isinstance(tarif, Tarif):
            continue  # Eğer tarif bir Tarif nesnesi değilse atla

        eslesen = set(secilen_urunler).intersection(tarif.malzemeler)
        if not tarif.malzemeler:  # Eğer tarifin malzemeleri boşsa sıfıra bölme hatasını önle
            yuzde = 0
        else:
            yuzde = len(eslesen) / len(tarif.malzemeler) * 100
        sonuclar.append((tarif.ad, round(yuzde, 2), list(set(tarif.malzemeler) - eslesen)))
    
    # Eşleşme yüzdesine göre sırala (yüksekten düşüğe)
    sonuclar = sorted(sonuclar, key=lambda x: x[1], reverse=True)
    
    return sonuclar









window = tk.Tk()
window.geometry("1000x600")
window.title("TARİF SİHİRBAZI")

# Dikey kaydırma çubuğu
vsb = Scrollbar(window, orient="vertical")
vsb.pack(side="right", fill="y")

# Yatay kaydırma çubuğu
hsb = Scrollbar(window, orient="horizontal")
hsb.pack(side="bottom", fill="x")

# Canvas widget'ı, içeriği kaydırmak için kullanılır
canvas = Canvas(window, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
canvas.pack(side="left", fill="both", expand=True)

# Dikey kaydırma çubuğunu canvas'a bağla
vsb.config(command=canvas.yview)

# Yatay kaydırma çubuğunu canvas'a bağla
hsb.config(command=canvas.xview)

# Canvas içindeki çerçeve, içerideki butonları düzenlemek için kullanılır
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')


#
#SEBZELER
#

# Tkinter etiketi oluşturuluyor
etiket = tk.Label(
    frame,
    text="Sebzeler",
    font="Tahoma 19",
    wraplength=500
)
etiket.grid(row=0, column=0, sticky="w", padx=10, pady=(20, 0))  # Etiketi sola üste taşı, üst boşluk 20, alt boşluk 0


# Buton adlarını içeren liste
sebzeler = ["Domates", "Salatalık", "Patates", "Soğan", "Yeşil Soğan", "Sarımsak", "Yeşil Biber","Kapya Biber", "Havuç", "Ispanak", "Turp","Nane","Taze Fasulye","Mısır","Dolmalık Biber","Pırasa","Mantar","Bezelye","Kabak","Bal Kabağı", "Brokoli",
 "Karnabahar","Kereviz","Enginar", "Asma Yaprağı","Kara Lahana", "Lahana", "Maydanoz", "Dereotu","Roka","Marul","Fesleğen","Marul","Bamya"]

# Butonları ekleyelim
for i, sebze in enumerate(sebzeler):
    button = tk.Button(frame, text=sebze)
    button['command'] = lambda s=sebze, b=button: button_click(s, b)
    button.grid(row=(i // 10) + 1, column=i % 10, padx=5, pady=5)
  


#
#MEYVELER
#


etiket = tk.Label(
    frame,
    text="Meyveler",
    font="Tahoma 19",
    wraplength=500
)
etiket.grid(row=5, column=0, sticky="w", padx=10, pady=(20, 0))  # Etiketi sola üste taşı, üst boşluk 20, alt boşluk 0

# Butonları ekleyelim (örnek için 10x10 bir ızgara)
# Buton adlarını içeren liste
meyveler = ["Elma", "Portakal", "Mandalina", "Limon","Çilek", "Muz","Şeftali", "Armut", "Ayva", "Greyfurt","Üzüm","Yaban Mersini","Ananas","Avakado","Nar","Karpuz","Hindistan Cevzi","İncir","Kivi", "Frambuaz",
 "Vişne","Kiraz","Erik","Kavun","Hurma","Mango"]

# Butonları ekleyelim
for i, meyve in enumerate(meyveler):
    button = tk.Button(frame, text=meyve)
    button['command'] = lambda m=meyve, b=button: button_click(m, b)
    button.grid(row=(i // 10) + 6, column=i % 10, padx=5, pady=5)
  

#
#HAYVANSAL GIDALAR
#


etiket = tk.Label(
    frame,
    text="Hayvansal Gıdalar ",
    font="Tahoma 19",
    wraplength=500
)
etiket.grid(row=10, column=0, sticky="w", padx=10, pady=(20, 0))  # Etiketi sola üste taşı, üst boşluk 20, alt boşluk 0

# Butonları ekleyelim (örnek için 10x10 bir ızgara)
# Buton adlarını içeren liste
hayvansal = ["Yumurta", "Kıyma", "Tavuk Göğüsü", "Tavuk Baget","Tavuk Kanat ", "Kuşbaşı Et", "Dana ciğer","Kuzu Eti","Hamsi", "Palamut", "Levrek", "Çinekop","Uskumru","Mezgit","Somon","Ton Balığı","Kuzu Kıyma","Kuzu pirzola","Hindi Eti","Dana Bonifile","Dana Antrikot","Sucuk","Sosis", "Kuru Et","Füme Et",
 "Jambon","Pastırma","Kalamar","Karides","Yengeç","Tavuk Suyu","Et Suyu","Balık Suyu"]

# Butonları ekleyelim
for i, hayvan in enumerate(hayvansal):
    button = tk.Button(frame, text=hayvan)
    button['command'] = lambda h=hayvan, b=button: button_click(h, b)
    button.grid(row=(i // 10) + 11, column=i % 10, padx=5, pady=5)
  

#
#Süt Ve Süt Ürünleri
#


etiket = tk.Label(
    frame,
    text="Süt Ürünleri",
    font="Tahoma 19",
    wraplength=500
)
etiket.grid(row=15, column=0, sticky="w", padx=10, pady=(20, 0))  # Etiketi sola üste taşı, üst boşluk 20, alt boşluk 0

# Butonları ekleyelim (örnek için 10x10 bir ızgara)
# Buton adlarını içeren liste
sütler = ["Margarin", "Tereyağı", "İnek Sütü", "Badem Sütü","Krema","Yoğut", "Süzme Yoğurt","Süzme Peynir", "Kaşar Peynir", "Mozzarella Peynir", "Ezine Peynir","Tulum Peynir","Labne Peynir","Mascarpone Peynir","Beyaz Peynir","Parmesan Peyniri","Kaymak","Cheddar Peynir","Kolot Peynir"]

# Butonları ekleyelim
for i, süt in enumerate(sütler):
    button = tk.Button(frame, text=süt)
    button['command'] = lambda s=süt, b=button: button_click(s, b)
    button.grid(row=(i // 10) + 16, column=i % 10, padx=5, pady=5)

#
#Bakliyat
#


etiket = tk.Label(
    frame,
    text="Bakliyat",
    font="Tahoma 19",
    wraplength=500
)
etiket.grid(row=20, column=0, sticky="w", padx=10, pady=(20, 0))  # Etiketi sola üste taşı, üst boşluk 20, alt boşluk 0

# Butonları ekleyelim (örnek için 10x10 bir ızgara)
# Buton adlarını içeren liste
bakliyat = ["Kuru fasulye","Meksika fasulyesi","Yeşil mercimek","Bakla","Maş fasulyesi","Kırmızı mercimek","Sarı mercimek","Kuru börülce","Barbunya","Nohut","Pirinç",
"Bulgur","Karabuğday","Risotto pirinci","Köftelik bulgur","Firik bulguru","Siyez Bulguru","İrmik"]

# Butonları ekleyelim
for i, bakla in enumerate(bakliyat):
    button = tk.Button(frame, text=bakla)
    button['command'] = lambda y=bakla, b=button: button_click(y, b)
    button.grid(row=(i // 10) + 21, column=i % 10, padx=5, pady=5)



#
# TAHILLAR
#


etiket = tk.Label(
    frame,
    text="Tahıllar ",
    font="Tahoma 19",
    wraplength=500
)
etiket.grid(row=25, column=0, sticky="w", padx=10, pady=(20, 0))  # Etiketi sola üste taşı, üst boşluk 20, alt boşluk 0

# Butonları ekleyelim (örnek için 10x10 bir ızgara)
# Buton adlarını içeren liste
tahillar = ["Un", "Mısır Unu", "Galeta Unu", "Buğday Nişastası", "Mısır Nişastası", "Tam Buğday Ekmeği", "Hamburger Ekmeği", "Tost Ekmeği", "Sandviç Ekmeği", "Bayat Ekmek",
 "Lavaş","Yufka", "Kepek Ekmeği", "Makarna", "Yulaf", "Mantı", "Şehriye", "Erişte", "Tarhana", "Lazanya", "Granola"]

# Butonları ekleyelim
for i, tahil in enumerate(tahillar):
    button = tk.Button(frame, text=tahil)
    button['command'] = lambda t=tahil, b=button: button_click(t, b)
    button.grid(row=(i // 10) + 26, column=i % 10,padx=5,pady=5)



#
#Baharat
#


etiket = tk.Label(
    frame,
    text="Baharatlar",
    font="Tahoma 19",
    wraplength=500
)
etiket.grid(row=30, column=0, sticky="w", padx=10, pady=(20, 0))  # Etiketi sola üste taşı, üst boşluk 20, alt boşluk 0


# Buton adlarını içeren liste
baharat = ["Kırmızı Tatlı Biber","Kırmızı Acı Biber","Kekik ", "Nane", "Kişniş", "Sumak", "Karabiber","Kimyon","Tarçın","Kabartma Tozu","Vanilya","Kakao","Hindistan Cevizi"]

# Butonları ekleyelim
for i, baharat in enumerate(baharat):
    button = tk.Button(frame, text=baharat)
    button['command'] = lambda x=baharat, b=button: button_click(x, b)
    button.grid(row=(i // 10) + 31, column=i % 10, padx=5, pady=5)

    


# Tarifleri göster butonu
show_recipes_button = tk.Button(window, text="Tarifleri Göster", command=lambda: sonuclari_goster())
show_recipes_button.pack(pady=10)



# Canvas'ın boyutunu ayarlamak için olay dinleyicisi
canvas.bind('<Configure>', on_configure)


window.mainloop()
