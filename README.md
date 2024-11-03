# BACKUP EQUIPAMENTOS MIKROTIK VIA ZABBIX 7.0
Backup de Equipamentos Mikrotik utilizando Zabbix 7.0

Esse tutorial foi desenvolvido por Anderson Reis utilizando o chat gpt.

Seu objetivo é fazer backup de equipamentos Mikrotik utilizando Zabbix 7.0

Para isso o Mikrotik deve ser acessível via SSH do servidor que contem o zabbix instalado.

Devemos primeiro instalar paramiko

```bash
apt update
apt install python3-paramiko
```

Primeiramente iremos criar um script em Python que utiliza a biblioteca Paramiko para acessar os equipamentos mikrotik e realizar o backup.

O script deve ser criado em: 

```python
cd /usr/lib/zabbix/externalscripts
nano backup_mk.py
```

Devemos dar permissão de execução para o script e também colocar como dono o usuário e grupo zabbix.

```python
chmod +x backup_mk.py
chown zabbix:zabbix backup_mk.py
```

Como o zabbix não entende python, devemos criar um script em Shell Script na mesma pasta anterior, para chamar o script em python e passar os parametros que serão recebidos do zabbix.

```python
cd /usr/lib/zabbix/externalscripts
nano backup_mikrotik.sh
```

Devemos dar permissão de execução para o script e também colocar como dono o usuário e grupo zabbix.

```python
chmod +x backup_mk.py
chown zabbix:zabbix backup_mikrotik.sh
```

Utilize o script backup_mikrotik.sh

Esse script recebe os mesmos 5 parâmetros do Zabbix

Devemos criar uma pasta que receberá os backups, essa pasta deverá ter dono e grupo zabbix.

```bash
mkdir /home/zabbix/backups
chown -R zabbix:zabbix /home/zabbix
```

Dentro do Zabbix 7 devemos importar o template que está com o nome: Template_Mikrotik_Backup_Zabbix_7.json

Agora basta inserir esse template no host que quiser.

Após inserir no host é necessário alterar alterar as Macros Herdadas, para que o script consiga acessar o Mikrotik

São 3 variáveis que devem ser alteradas

```bash
{$USERNAME} = inserir o usuario do mikrotik
{$PASSWORD} = inserir a senha do mikrotik
{$BACKUP_DIR} = inserir o diretorio configurado anteriormente /home/zabbix/backups
```

Por padrão o template está configurado para executar o script 1 vez ao dia a 1 hora da manhã.