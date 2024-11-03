#Backup de Equipamentos MikroTik via Zabbix 7.0
Desenvolvido por Anderson Reis com a ajuda do ChatGPT

Este tutorial tem como objetivo ensinar como realizar o backup de equipamentos MikroTik utilizando o Zabbix 7.0. O processo envolve a configuração de scripts em Python e Shell, além da integração com o Zabbix para automatizar as tarefas de backup.

##Pré-requisitos
Servidor com Zabbix 7.0 instalado.
Acesso SSH aos equipamentos MikroTik a partir do servidor Zabbix.
Conhecimentos básicos em Linux, Python e Shell Script.

##Passo 1: Atualizar o Sistema e Instalar o Paramiko
Primeiramente, atualize os pacotes do sistema e instale a biblioteca paramiko, que será utilizada para comunicação SSH com os equipamentos MikroTik.

```bash
sudo apt update
sudo apt install python3-paramiko -y
```

##Passo 2: Criar o Script em Python para Backup
O script em Python utilizará a biblioteca Paramiko para acessar os equipamentos MikroTik e realizar o backup.

Navegue até o diretório de scripts externos do Zabbix:

Cole o arquivo backup_mk.py dentro do diretorio abaixo:

```bash
cd /usr/lib/zabbix/externalscripts
```

Dê permissão de execução e ajuste o dono/grupo do script:

```bash
sudo chmod +x /usr/lib/zabbix/externalscripts/backup_mk.py
sudo chown zabbix:zabbix /usr/lib/zabbix/externalscripts/backup_mk.py
```

##Passo 3: Criar o Script Shell para Integração com o Zabbix
Como o Zabbix não interpreta diretamente scripts Python, criaremos um script Shell que chama o script Python, passando os parâmetros necessários.

No mesmo diretório de scripts externos, crie ou copie o arquivo arquivo backup_mikrotik.sh:

```bash
cd /usr/lib/zabbix/externalscripts
```

Dê permissão de execução e ajuste o dono/grupo do script:

```bash
sudo chmod +x /usr/lib/zabbix/externalscripts/backup_mikrotik.sh
sudo chown zabbix:zabbix /usr/lib/zabbix/externalscripts/backup_mikrotik.sh
```

##Passo 4: Configurar o Diretório de Backups
Crie um diretório onde os backups serão armazenados e ajuste as permissões adequadamente.

```bash
sudo mkdir -p /home/zabbix/backups
sudo chown -R zabbix:zabbix /home/zabbix
sudo chmod -R 750 /home/zabbix/backups
```

##Passo 5: Importar e Configurar o Template no Zabbix
Acesse a interface web do Zabbix com uma conta administrativa.

Navegue até Configuration (Configuração) > Templates (Templates).

Clique em Import (Importar) e selecione o arquivo Template_Mikrotik_Backup_Zabbix_7.json.

Após a importação, vá para Configuration (Configuração) > Hosts (Hosts) e selecione o host MikroTik que deseja configurar.

Clique em Templates (Templates) e adicione o template Template_Mikrotik_Backup_Zabbix_7 ao host.

##Passo 6: Configurar as Macros no Host
Para que o script possa acessar o MikroTik, é necessário configurar as macros herdadas no host.

No host MikroTik, vá para a aba Macros.

Configure as seguintes macros:

{$USERNAME}: Insira o usuário SSH do MikroTik.
{$PASSWORD}: Insira a senha SSH do MikroTik.
{$BACKUP_DIR}: Insira o diretório de backups configurado anteriormente (/home/zabbix/backups).

##Passo 7: Agendar a Tarefa de Backup
Por padrão, o template está configurado para executar o script uma vez ao dia, às 1 hora da manhã. Caso deseje alterar o agendamento:

No host MikroTik, navegue até Configuration (Configuração) > Templates (Templates).

Selecione o template Template_Mikrotik_Backup_Zabbix_7 e edite o Item (Item) ou Trigger (Gatilho) responsável pelo agendamento.

Ajuste o Intervalo de atualização conforme sua necessidade (por exemplo, para executar diariamente às 1h da manhã, mantenha o agendamento padrão ou ajuste conforme preferir).

##Passo 8: Testar a Configuração
Após configurar tudo, é importante testar se o backup está funcionando corretamente.

No Zabbix, vá até Monitoring (Monitoramento) > Latest Data (Últimos Dados).

Selecione o host MikroTik e verifique os itens relacionados ao backup.

Verifique se os backups estão sendo salvos no diretório /home/zabbix/backups com os nomes apropriados.

Caso haja erros, verifique os logs do Zabbix e ajuste as permissões ou configurações conforme necessário.

##Dicas de Segurança
Permissões: Garanta que apenas o usuário zabbix tenha acesso aos scripts e diretórios de backup.

Backups Remotos: Considere armazenar backups em um local remoto ou serviço de armazenamento seguro para proteção adicional.

##Conclusão
Com este tutorial, você configurou com sucesso o backup automático de equipamentos MikroTik utilizando o Zabbix 7.0. Manter backups regulares é essencial para garantir a recuperação rápida em caso de falhas ou configurações incorretas. Lembre-se de monitorar regularmente os backups e testar a restauração para assegurar que tudo está funcionando conforme o esperado.

Caso tenha dúvidas ou encontre problemas durante a configuração, não hesite em consultar a documentação oficial do Zabbix ou buscar suporte na comunidade.