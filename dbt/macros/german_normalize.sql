{% macro german_normalize(text_col) %}
    regexp_replace(
        regexp_replace(
            regexp_replace(
                regexp_replace(
                    regexp_replace(
                        regexp_replace(
                            regexp_replace(
                                regexp_replace(
                                    regexp_replace(
                                        regexp_replace(
                                            regexp_replace(
                                                regexp_replace(
                                                    regexp_replace(
                                                        regexp_replace(
                                                            regexp_replace(
                                                                regexp_replace(
                                                                    regexp_replace(
                                                                        regexp_replace(
                                                                            regexp_replace(
                                                                                regexp_replace(
                                                                                    regexp_replace(
                                                                                        regexp_replace(
                                                                                            regexp_replace(
                                                                                                regexp_replace(
                                                                                                    regexp_replace(
                                                                                                        regexp_replace(
                                                                                                            regexp_replace(
                                                                                                                regexp_replace(
                                                                                                                    regexp_replace(
                                                                                                                        regexp_replace(
                                                                                                                            regexp_replace(
                                                                                                                                regexp_replace(
                                                                                                                                    regexp_replace(
                                                                                                                                        regexp_replace(
                                                                                                                                            regexp_replace(
                                                                                                                                                regexp_replace(
                                                                                                                                                    regexp_replace(
                                                                                                                                                        regexp_replace(
                                                                                                                                                            regexp_replace(
                                                                                                                                                                regexp_replace(
                                                                                                                                                                    regexp_replace(
                                                                                                                                                                        regexp_replace(
                                                                                                                                                                            regexp_replace(
                                                                                                                                                                                regexp_replace(
                                                                                                                                                                                    regexp_replace(
                                                                                                                                                                                        regexp_replace(
                                                                                                                                                                                            regexp_replace(
                                                                                                                                                                                                regexp_replace(
                                                                                                                                                                                                    regexp_replace(
                                                                                                                                                                                                        regexp_replace(
                                                                                                                                                                                                            regexp_replace(
                                                                                                                                                                                                                regexp_replace(
                                                                                                                                                                                                                    regexp_replace(
                                                                                                                                                                                                                        regexp_replace(
                                                                                                                                                                                                                            regexp_replace(
                                                                                                                                                                                                                                regexp_replace(
                                                                                                                                                                                                                                    regexp_replace(
                                                                                                                                                                                                                                        regexp_replace(
                                                                                                                                                                                                                                            regexp_replace(
                                                                                                                                                                                                                                                regexp_replace(
                                                                                                                                                                                                                                                    regexp_replace(
                                                                                                                                                                                                                                                        regexp_replace(
                                                                                                                                                                                                                                                            regexp_replace(
                                                                                                                                                                                                {{ text_col }}, 'ü', 'ue'),
                                                                                                                                                                                            'Ü', 'Ue'),
                                                                                                                                                                                        'ö', 'oe'),
                                                                                                                                                                                    'Ö', 'Oe'),
                                                                                                                                                                                'ä', 'ae'),
                                                                                                                                                                            'Ä', 'Ae'),
                                                                                                                                                                        'ß', 'ss'),
                                                                                                                                                                    'Prüf\\.', 'Pruefung'),
                                                                                                                                                                'Lagerstörung', 'Lagerstoerung'),
                                                                                                                                                            'Instandhaltung', 'Maintenance'),
                                                                                                                                                        'Wartung', 'Service'),
                                                                                                                                                    'Störung', 'Stoerung'),
                                                                                                                                                'LKW', 'Truck'),
                                                                                                                                            'München', 'Muenchen'),
                                                                                                                                        'Göttingen', 'Goettingen'),
                                                                                                                                    'Düsseldorf', 'Duesseldorf'),
                                                                                                                                'Köln', 'Koeln'),
                                                                                                                            'Leipzig', 'Leipzig'),
                                                                                                                        'Betrieb', 'Operation'),
                                                                                                                    'erforderlich', 'required'),
                                                                                                                'abgeschlossen', 'completed'),
                                                                                                            'normal', 'normal'),
                                                                                                        'erkannt', 'detected'),
                                                                                                    'Kosten', 'Cost'),
                                                                                                'Standort', 'Location'),
                                                                                            'Anlage', 'Asset'),
                                                                                        'Datum', 'Date'),
                                                                                    'Status', 'Status'),
                                                                                'EUR', 'EUR'),
                                                                            'Instandhaltung erforderlich', 'Maintenance required'),
                                                                        'Wartung abgeschlossen', 'Service completed'),
                                                                    'Betrieb normal', 'Operation normal'),
                                                                'Störung erkannt', 'Fault detected')
    )
{% endmacro %}
{% endmacro %}
