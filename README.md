# odoo14_material
Module for registering and managing materials

## developer
muhamadalfarisy98@gmail.com

## How to?
```bash
#run unit test
python3 odoo-bin --test-enable -d <namadb> -i odoo14_material --update odoo14_material

#atau
python3 odoo-bin --test-enable -d <namadb>

```

## Debug mode (launch.json) && unit test
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Odoo 14",
            "type": "python",
            "request": "launch",
            "stopOnEntry": false,
            "python": "/home/farisy/Envs/odoo14/bin/python",
            "console": "integratedTerminal",
            "program": "/opt/odoo/odoo14/odoo-bin",
            "args": [
                "--config=/opt/odoo/config/odoo14.conf",
                "--dev=all",
                "--test-enable",
                "-i", "odoo14_material",
                "--test-tags=material_unittest",

                // "--db-filter=db_test_clean" 

                // "--stop-after-init",
                // "--update=odoo14_material",
            ]
        }
    ]
}


```

## ERD 
<img width="456" height="218" alt="erd" src="https://github.com/user-attachments/assets/1d47ada8-9c78-4902-a164-8edeed01393a" />

explaination : in odoo V14, if a record of res.partner ever has created an PO, the `supplier_rank` will increase its number (must enable purchase module first). if `supplier_rank` > 0, it means the res.partner record is `supplier`. So no need to add new custom field on res.partner


## API Doc
## [1] Get Materials
1. success

`curl --location 'http://localhost:8069/api/materials'`

<img width="1027" height="851" alt="image" src="https://github.com/user-attachments/assets/ace6b55e-f873-48c3-bf6f-df1b68ac31e2" />

2. filter by material_type

`curl --location 'http://localhost:8069/api/materials?material_type=fabrics'`

<img width="1005" height="628" alt="image" src="https://github.com/user-attachments/assets/d7cfcd5c-c39d-4746-a2a4-a6d81500637b" />



## [2] Add Materials

## [3] Delete Material
1. success

`curl --location --request DELETE 'http://localhost:8069/api/materials/4`

<img width="1049" height="569" alt="image" src="https://github.com/user-attachments/assets/467444e6-9b7d-4735-8209-99ec65867b7f" />


2. Not found

`curl --location --request DELETE 'http://localhost:8069/api/materials/3'`

<img width="898" height="519" alt="image" src="https://github.com/user-attachments/assets/67404eef-6487-49d6-879c-6b62cf121889" />



## [4] Update Materials



## [1] Endpoints Credit (Deposit)
