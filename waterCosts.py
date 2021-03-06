
class waterCosts:
    def __init__(self):
        # Costs per gallon in different cities:
        
        # Average person uses 100 gallons of water per day
        # (http://www.epa.gov/WaterSense/pubs/indoor.html; accessed Aug 2014)    
        # The average household (family of 4) uses 12,000 gallons per month
        
        # Austin charges $9.95 per 1000 gallons for 11,001 - 20,000 total
        # gallons of usage per month
        # (http://www.austintexas.gov/department/austin-water-utility-service-rates; accessed Aug 2014)
        self.austin = 9.95/1000.

        # San Antonio charges $0.1529 per 100 gallons for 12,717 - total 
        # gallons of usage per month 
        # This is the seasonal rate (approx. May through Sept.)
        # (http://www.saws.org/service/rates/Resident.cfm - accessed August 2014)
        self.sanAntonio = 0.1529/100.
        
        # Dallas charges 5.20 per 1,000 gallons for the range of 10,001 to 15,000 gallons
        # gallons of usage per month
        # (http://www.dallascityhall.com/dwu/billing_rates_monthly.html; accessed Aug 2014)
        self.dallas = 5.20/1000.
        
        # Houston charges 7.44 per 1,000 gallons for over 6,000 gallons
        # gallons of usage per month
        # (http://edocs.publicworks.houstontx.gov/documents/divisions/resource/ucs/2014_water_rates.pdf; accessed Aug 2014)
        self.houston = 7.44/1000.
