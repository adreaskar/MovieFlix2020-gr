# MovieFlix

### Περιεχόμενα

- [Τι είναι το MovieFlix?](https://github.com/adreaskar/MovieFlix2020_E17067_Karabetian_Andreas#%CF%84%CE%AF-%CE%AD%CE%B9%CE%BD%CE%B1%CE%B9-%CF%84%CE%BF-movieflix)
- [Πώς λειτουργεί](https://github.com/adreaskar/MovieFlix2020_E17067_Karabetian_Andreas#%CE%BB%CE%B5%CE%B9%CF%84%CE%BF%CF%85%CF%81%CE%B3%CE%AF%CE%B5%CF%82)
- [Πώς μπορώ να το χρησιμοποιήσω?](https://github.com/adreaskar/MovieFlix2020_E17067_Karabetian_Andreas#%CF%80%CF%8E%CF%82-%CE%BC%CF%80%CE%BF%CF%81%CF%8E-%CE%BD%CE%B1-%CF%84%CE%BF-%CF%87%CF%81%CE%B7%CF%83%CE%B9%CE%BC%CE%BF%CF%80%CE%BF%CE%B9%CE%AE%CF%83%CF%89)

## Τι έιναι το MovieFlix
Είναι ένα Web Service, μία βάση δεδομένων που αποθηκεύονται οι εγγεγραμμένοι χρήστες αλλά και πληροφορίες για ταινίες. 

Αυτές να είναι:

- Τίτλος
- Έτος κυκλοφορίας
- Πλοκή
- Ηθοποιοί 
- Κριτική
- Σχόλια χρηστών

Ο εγγεγραμμένος χρήστης έχει ένα φάσμα ενεργειών που μπορεί να πραγματοποιήσει:

- Αναζήτηση μιας ταινίας και εμφάνιση των πληροφοριών της.
- Βαθμολόγηση και σχολιασμός στην σελίδα μιας ταινίας.
- Προβολή όλων των σχολίων και βαθμολογιών που έχει κάνει καθώς και διαγραφή αυτών.
- Διαγραφή του λογαριασμού του.

Παρέχεται στους χρήστες προστασία των δεδομένων τους με κρυπτογράφηση του κωδικού του κάθε λογαριασμού.

## Λειτουργίες

## Πώς μπορώ να το χρησιμοποιήσω

:pushpin: **Κατέβασμα εφαρμογής**

Για να χρησιμοιποιήσετε την εφαρμογή πρέπει να κατεβάσετε τα αρχεία του Repository στον υπολογιστή σας. Αυτό μπορεί να γίνει εύκολα κατεβάζοντας τα ως .zip αρχείο, όπως φαίνεται παρακάτω.

![download](https://github.com/adreaskar/images/blob/master/download.jpg?raw=true)

:pushpin: **Εγκατάσταση docker / docker-compose**

Το εργαλείο που θα χρησιμοποιήσουμε για να τρέξουμε την εφαρμογή είναι το Docker. Για την εγκατάσταση του παραθέτω τα βήματα που έχει και στην ιστοσελίδα του.

Ανοίγουμε το terminal και τρέχουμε την παρακάτω εντολή για να διαγράψουμε τυχόν παλιές εκδόσεις του docker που μπορεί να υπάρχουν στο σύστημα μας.

```
$ sudo apt-get remove docker docker-engine docker.io containerd runc
```

Αναβάθμιση του `apt` και εγκατάσταση πακέτων 

```
$ sudo apt-get update

$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

Προσρθήκη του Docker GPG key

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Προσθήκη του repository

```
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

Και τέλος αφού φτιάξαμε το repository του docker, απλά το εγκαθιστούμε

```
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Για την εγκατάσταση του docker-compose θα χρειαστούν οι παρακάτω δύο εντολές

```
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

$ sudo chmod +x /usr/local/bin/docker-compose

```
Και είμαστε έτοιμοι να τρέξουμε την εφαρμογή!

:pushpin: **Εκκίνηση εφαρμογής**

1. Πηγαίνουμε στο directory που κατεβάσαμε το zip στο πρώτο βήμα και το κανουμε extract.
2. Ανοίγουμε τον φάκελο _MovieFlix2020_E17067_Karabetian_Andreas_ καθώς και τον φάκελο _Project_ που έχει μέσα του.
3. Τώρα πρέπει να βλέπουμε έναν φάκελο _flask_ και ένα αρχείο _docker-compose.yml_.
4. Εδώ ανοίγουμε ένα terminal και γράφουμε την εντολή `$ sudo docker-compose up -d` για την εκκίνηση της εφαρμογής.

Το πρόγραμμα θα αρχίσει να φτιάχνει τα απαραίτητα αρχεία που χρειάζεται και θα έχει τελειώσει όταν δούμε το σχετικό μήνυμα όπως φαίνεται παρακάτω.

![done](https://github.com/adreaskar/images/blob/master/done.jpg?raw=true)

## Πλέον μπορούμε να χρησιμοποιήσουμε την εφαρμογή ανοίγοντας έναν browser και πλητρολογώντας την διεύθυνση "localhost:5000"
