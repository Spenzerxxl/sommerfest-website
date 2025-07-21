try {
    // GET-REQUEST-LÖSUNG: Direkt zu n8n-Webhook
    const searchParams = new URLSearchParams();
    searchParams.append('name', formData.name);
    searchParams.append('email', formData.email);
    searchParams.append('lodge', formData.lodge);
    searchParams.append('companions', formData.companions);
    searchParams.append('contribution', formData.contribution);
    searchParams.append('quantity', formData.quantity);
    
    const response = await fetch(`${N8N_WEBHOOK_URL}?${searchParams}`, {
        method: 'GET',
        mode: 'no-cors'  // Verhindert CORS-Probleme
    });

    // Bei no-cors können wir Status nicht prüfen - daher Success annehmen
    console.log('Anmeldung gesendet:', formData);
    
    // Neue Beiträge zur lokalen Liste hinzufügen
    const buffetItems = JSON.parse(formData.contribution);
    buffetItems.forEach(item => {
        contributions.push({
            item: item.item,
            quantity: item.quantity
        });
    });
    updateContributionsList();

    // Erfolgsanzeige
    document.getElementById('successMessage').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';

    // Formular zurücksetzen
    this.reset();
    
    // Dynamische Buffet-Felder zurücksetzen
    const dynamicItems = document.querySelectorAll("[id^=contribution][id!=contribution], [id^=quantity][id!=quantity]");
    dynamicItems.forEach(item => item.parentNode.remove());
    buffetItemCount = 1;
    
    // Nach 5 Sekunden Erfolgsmeldung ausblenden
    setTimeout(() => {
        document.getElementById('successMessage').style.display = 'none';
    }, 5000);
    
} catch (error) {
    console.error('Fehler beim Senden:', error);
    document.getElementById("errorMessage").textContent = "Fehler beim Senden der Anmeldung. Bitte versuchen Sie es erneut.";
    document.getElementById("errorMessage").style.display = "block";
    document.getElementById("successMessage").style.display = "none";
}
