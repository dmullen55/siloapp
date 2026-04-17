def fetch_silos(self):
        container = self.root_sm.get_screen('silo_view').ids.silo_container
        container.clear_widgets()
        
        try:
            # TEST 1: Can we even reach Google?
            test_resp = requests.get("https://www.google.com", timeout=5)
            container.add_widget(Label(text=f"Google Reachable: {test_resp.status_code}"))
            
            # If Google works, then we try Supabase again
            headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/silos?select=*", 
                headers=headers, 
                timeout=10,
                verify=certifi.where()
            )
            
            if response.status_code == 200:
                container.add_widget(Label(text="✅ Supabase Connected!"))
            else:
                container.add_widget(Label(text=f"❌ Supabase HTTP {response.status_code}"))
                
        except Exception as e:
            # This will tell us if it's a 'DNS' or 'Connection' error
            container.add_widget(Label(text=f"FAIL: {str(e)[:45]}", color=(1,0,0,1)))
