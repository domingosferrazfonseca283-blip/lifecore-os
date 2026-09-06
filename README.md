# LIFECORE OS

Sistema experimental de computação viva modular, desenvolvido primeiro em Termux e evoluindo em direção a controle de sistema e hardware.

## V1.2.0

Base validada em telefone Android:
- percepção de bateria, temperatura e Wi-Fi
- diagnóstico de saúde
- eventos e tendências
- memória persistente SQLite
- memória contextual
- decisões/reflexos com camada de segurança
- estado persistente
- LIFE ENGINE integrando percepção, memória, contexto, tendências e decisão

## Arquitetura

```text
LIFECORE OS
  ↓
LIFE ENGINE
  ↓
SYSTEM CONTROL
  ↓
HAL / DRIVERS
  ↓
KERNEL
  ↓
HARDWARE
```

## Princípios

- GitHub é a fonte oficial do código.
- Termux é o laboratório de execução e validação no telefone.
- Dados de runtime e memória pessoal não são versionados.
- Ações potencialmente perigosas não são executadas sem uma camada explícita de segurança.

## Próxima etapa

V1.3: histórico temporal estruturado, desenvolvido somente após sincronização e validação da V1.2.0.
