from __future__ import print_function


# US states and abbreviation
# Code Written by Sameer Sam0hack <sam.nyx@live.com>
# version 1.0

def abbreviations(val):
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
              "District of Columbia",
              "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
              "Maine",
              "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
              "North Carolina",
              "North Dakota", "Ohio", "Oklahoma", "Oregon", "Maryland", "Massachusetts", "Michigan", "Minnesota",
              "Mississippi",
              "Missouri", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
              "Utah",
              "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    abbreviation = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    if len(val) == 2:
        val = val.upper()
        if val in abbreviation:
            return val

        else:
            return False
        pass
    elif len(val) > 2:
        val = val.title()
        if val in states:
            if ' ' in val:
                cval = val.upper().split()
                cval = cval[0][0] + cval[1][0]
                if cval in abbreviation:
                    return cval
                else:
                    return False
                pass
            else:
                v1 = val[0].upper()
                v2 = val[1].upper()
                v2 = v1 + v2
                return v2
        else:
            return False
        pass
    else:
        return False
