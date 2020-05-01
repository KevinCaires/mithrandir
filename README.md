# Mithrandir

### Proposta

A API mithrandir foi criada com a intenção de fornecer suporte à criação e manutenção de ordens de serviço para o aplicativo `Startup Me`, aplicativo a ser apresentado para o TCC nas Faculdades Integradas Camões. Nessa API é utilizado os FrameWorks Django e Graphql.

### Compatível com o sistemas
![Linux Badges](https://img.shields.io/badge/OS-Linux-black)

### Linguagem

![Python Badge](https://img.shields.io/badge/Python-3.6.9-black)

### Dependências

As dependencias e pacotes necessários estão contidas no arquivo `dev.txt` dentro do diretório requirements.




## Consultas Graphql

### `Creates`

Mutation que cria EPI's no sistema:
```
mutation{
  createPersonalProtectiveEquipment(input:{
    name:"Some name"
    equipmentModel:"Some model"
    serialNumber:"Some serial number"
    description:"Some description"
  }){
    personalProtectiveEquipment{
      id
      name
      equipmentModel
      serialNumber
      description
    }
  }
}
```

Mutation que cria equipamentos da atividate:
```
mutation{
  createJobEquipment(input:{
    name:"Some name"
    description:"Some description"
    equipmentModel:"Some model"
    serialNumber:"Some serial number"
  }){
    jobEquipment{
      id
      name
      equipmentModel
      serialNumber
      description
    }
  }
}
```

Mutation que cria o tipo de atividade:
```
mutation{
  createJobGroup(input:{
    name:"Some name"
    description:"Some description"
  }){
    jobGroup{
      id
      name
      description
    }
  }
}
```

Mutation que cria a atividade:
```
mutation{
   createJob(input:{
    name:"Some name",
    perMeter:true 'or' false
    valuePerMeter:Some float value
    jobGroupId:"Some job group id"
    jobEquipmentId:"Some job equipment id"
    hasPpe:false 'or' false
    ppeId:"Some personal protective equipment id"
  }){
    job{
      id
      name
      perMeter
      valuePerMeter
      jobGroup{
        id
        name
        description
      }
      jobEquipment{
        id
        name
        equipmentModel
        serialNumber
        description
      }
      hasPpe
      ppe{
        id
        name
        equipmentModel
        serialNumber
        description
      }      
    }
  }
}
```

Mutation que cria uma ordem de serviço:
```
mutation{
  createServiceOrder(input:{
    title:"Some title"
    description:"Some description"
    perMeter:Some boolean
    jobId:"Some job id"
  }){
    serviceOrder{
      id
      title
      description
      openDate
      perMeter
      jobId{
        id
        name
        perMeter
        valuePerMeter
        jobGroup{
          id
          name
          description
        }
        hasPpe
        ppe{
          id
          name
          equipmentModel
          serialNumber
          description
        }
        jobEquipment{
          id
          name
          equipmentModel
          serialNumber
          description
        }
      }
    }
  }
}
```

### `Queries`

Query que retorna as EPI's cadastradas no sistema: 
```
query{
  personalProtectiveEquipment{
    edges{
      node{
        id
        name
        equipmentModel
        serialNumber
        description
      }
    }
  }
}
```

Query que retorna os equipamentos de trabalho cadastrados:
```
query{
  jobEquipment{
    edges{
      node{
        id
        name
        equipmentModel
        serialNumber
        description
      }
    }
  }
}
```

Query que retorna os tipos de atividades cadastradas:
```
query{
  jobGroup{
    edges{
      node{
        id
        name
        description
      }
    }
  }
```

Query que retorna uma atividade com seu tipo e equipamentos cadastrados:
```
query{
  job{
    edges{
      node{
        id
        name
        perMeter
        valuePerMeter
        jobGroup{
          id
          name
          description
        }
        hasPpe
        ppe{
          id
          name
          equipmentModel
          serialNumber
          description
        }
        jobEquipment{
          id
          name
          serialNumber
          description
        }
      }
    }
  }
}
```

Query que retorna as ordens de serviço criadas:
```
query{
  serviceOrder{
    edges{
      node{
        id
        title
        description
        openDate
        perMeter
        closeDate
        serviceValue
        jobId{
          id
          name
          perMeter
          valuePerMeter
          jobGroup{
            id
            name
            description
          }
          hasPpe
          ppe{
            id
            name
            equipmentModel
            serialNumber
            description
          }
          jobEquipment{
            id
            name
            equipmentModel
            serialNumber
            description
          }
        }
      }
    }
  }
}
```

### `Updates`

Mutation que edita as EPI's do sistena:
```
mutation{
  updatePersonalProtectiveEquipment(input:{
    id:"Some id",
    name:"Some name",
    equipmentModel:"Some model",
    description:"Some description"
  }){
    personalProtectiveEquipment{
      id
      name
      equipmentModel
      serialNumber
      description
    }
  }
}
```

Mutation que edita os Equipamentos do sistema:
```
mutation{
  updateJobEquipment(input:{
    id:"Some id",
    name:"Some name",
    description:"Some description",
    equipmentModel:"Some model",
    serialNumber:"Some serial number"
  }){
    jobEquipment{
      id
      name
      description
      serialNumber
    }
  }
}
```

Mutation que edita o grupo de atividades:
```
mutation{
  updateJobGroup(input:{
    id:"Some id"
    description:"Some description"
  }){
    jobGroup{
      id
      name
      description
    }
  }
}
```

Mutation que edita a atividade:
```
mutation{
  updateJob(input:{
    id:"Some id",
    perMeter:false 'or' true
    valuePerMeter:Some float
    jobGroupId:"Some job group id"
    jobEquipmentId:"Some job equipment id"
    hasPpe:false 'or' true
    ppeId:"Some personal protective equipment"
  }){
    job{
      id
      name
      perMeter
      valuePerMeter
      jobGroup{
        id
        name
        description
      }
      hasPpe
      ppe{
        id
        name
        equipmentModel
        serialNumber
        description
      }
      jobEquipment{
        id
        name
        equipmentModel
        serialNumber
        description
      }
    }
  }
}
```

Mutation que edita a ordem de serviço:
```
mutation{
  updateServiceOrder(input:{
    id:"Some id"
    title:"Some title"
    description:"Some description"
    jobId:"Some job id"
    serviceValue: Some float value 
  }){
    serviceOrder{
      id
      title
      description
      serviceValue
      perMeter
      jobId{
        id
        name
        perMeter
        valuePerMeter
        jobGroup{
          id
          name
          description
        }
        hasPpe
        ppe{
          id
          name
          equipmentModel
          serialNumber
          description
        }
        jobEquipment{
          id
          name
          equipmentModel
          serialNumber
          description
        }
      }
    }
  }
}
```
