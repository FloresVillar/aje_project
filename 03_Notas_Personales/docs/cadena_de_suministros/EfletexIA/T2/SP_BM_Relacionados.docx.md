#### SP BM Relacionados.docx

**SP BM Relacionado**

**Envio de Pedidos y Clientes**  
Store procedure que envía información de los pedidos hacia EfletexIA y tambien incluye lista de clientes programados en cada viaje.

**Stored Procedure: COM_PREPARAR_CARGA_PEDIDO_PLINT**

```sql
ALTER PROCEDURE [dbo].[COM_PREPARAR_CARGA_PEDIDO_PLINT]
@COMPANIA CHAR(4),
@SUCURSAL CHAR(4),
@EMISOR CHAR(4),
@ZONA NVARCHAR(max),
@ID INT

AS
BEGIN

    --EXEC [COM_PREPARAR_CARGA_PEDIDO_PLINT] '0076','08','02','31000'
    SET NOCOUNT ON;

    DECLARE @V_XML XML;
    DECLARE @v_eXML varchar (max);
    DECLARE @Pais char(2);

    -- CREAMOS TEMPORAL CON LAS ZONAS A BUSCAR
    CREATE TABLE #TMP_ZONAS (
        ZONA INT
    )
    INSERT INTO #TMP_ZONAS(ZONA)
    SELECT * FROM dbo.Split(@ZONA, ',')

    DECLARE @FECDISTRIB INT, @FECPREVTA INT, @EFFACTUR CHAR(3), @EPASSTOCK CHAR(3)

    SELECT @FECDISTRIB=FECDISTRIB, @FECPREVTA=FECPREVTA
    FROM MEMIS01F WITH (NOLOCK)
    WHERE COMPANIA=@COMPANIA AND SUCURSAL=@SUCURSAL AND EMISOR=@EMISOR

    --set @fecprevta=dbo.fc_integerdate('04/02/2010')
    --set @fecdistrib=dbo.fc_integerdate('05/02/2010')

    SELECT @EFFACTUR=EFFACTUR, @EPASSTOCK = EPASSTOCK
    FROM MPADIS1F WITH (NOLOCK)
    WHERE COMPANIA=@COMPANIA

    ---------------------------------------------------------------------------
    -- Se realiza envio de data de clientes para los pedidos seleccionados --
    ---------------------------------------------------------------------------
    DECLARE @CTE_X_PEDI INT, @CTE_X_INTE INT

    SELECT clienteID, CODFVTA3
    INTO #CLIENTES_PEDIDO
    FROM (
        SELECT DISTINCT A.CLIENTE AS clienteID, E.CODFVTA3
        FROM TPEDID2F A WITH (NOLOCK)
        INNER JOIN MARTIC1F B WITH (NOLOCK) ON A.COMPANIA=B.COMPANIA AND A.ARTICULO=B.ARTICULO
        INNER JOIN TPEDID1F E WITH (NOLOCK) ON A.COMPANIA=E.COMPANIA AND 
            A.SUCURSAL=E.SUCURSAL AND A.TIPO=E.TIPO AND A.NRODOC=E.NRODOC
            A.SUCURSAL=E.SUCURSAL AND A.EMISOR=E.EMISOR AND 
            A.DOCUPEDIDO=E.DOCUPEDIDO AND 
            A.NROPEDIDO=E.NROPEDIDO AND E.FECPEDIDO=@FECPREVTA
        LEFT JOIN MCLIEN4F D WITH (NOLOCK) ON A.COMPANIA=D.COMPANIA AND 
            A.SUCURSAL=D.SUCURSAL AND A.CLIENTE=D.CLIENTE AND E.CODFVTA3=D.CODFVTA3
        INNER JOIN MLINEA1F F WITH (NOLOCK) ON B.COMPANIA=F.COMPANIA AND 
            B.LINEA=F.LINEA AND F.FLGLINEA='Te'
        INNER JOIN #TMP_ZONAS c ON a.ZONADIST = c.ZONA
        WHERE A.COMPANIA=@COMPANIA and A.SUCURSAL=@SUCURSAL and A.EMISOR=@EMISOR and 
        a.stspederr='N' AND
            --A.ZONADIST=ISNULL(@ZONA,A.ZONADIST) and
            A.FLGASIGNAC='S' AND COALESCE(A.DOCUCOMALM,'')='' AND
            COALESCE(A.NROCOMALM,'')='' AND A.STSPEDIDO=@EPASSTOCK
            AND ISNULL(E.ORIGPEDIDO, '') NOT IN ('011')
        UNION ALL
        SELECT DISTINCT A.CLIENTE AS clienteID, E.CODFVTA3
        FROM TPEDID2F A WITH (NOLOCK)
        INNER JOIN MARTIC1F B WITH (NOLOCK) ON A.COMPANIA=B.COMPANIA AND 
            A.ARTICULO=B.ARTICULO
        INNER JOIN TPEDID1F E WITH (NOLOCK) ON A.COMPANIA=E.COMPANIA AND 
            A.SUCURSAL=E.SUCURSAL AND A.EMISOR=E.EMISOR AND 
            A.DOCUPEDIDO=E.DOCUPEDIDO AND 
            A.NROPEDIDO=E.NROPEDIDO 
            AND E.FECENTREGA = @FECDISTRIB
        LEFT JOIN MCLIEN4F D WITH (NOLOCK) ON A.COMPANIA=D.COMPANIA AND 
            A.SUCURSAL=D.SUCURSAL AND A.CLIENTE=D.CLIENTE AND E.CODFVTA3=D.CODFVTA3
        INNER JOIN MLINEA1F F WITH (NOLOCK) ON B.COMPANIA=F.COMPANIA AND 
            B.LINEA=F.LINEA AND F.FLGLINEA='Te'
        INNER JOIN #TMP_ZONAS c ON a.ZONADIST = c.ZONA
        WHERE A.COMPANIA=@COMPANIA and A.SUCURSAL=@SUCURSAL and A.EMISOR=@EMISOR and 
        a.stspederr='N' AND
            --A.ZONADIST=ISNULL(@ZONA,A.ZONADIST) and
            A.FLGASIGNAC='S' AND COALESCE(A.DOCUCOMALM,'')='' AND
            COALESCE(A.NROCOMALM,'')='' AND A.STSPEDIDO=@EPASSTOCK
            AND E.ORIGPEDIDO = '011') AS A

    SELECT DISTINCT clienteID, CODFVTA3
    INTO #CLIENTES_INTEGRA
    FROM #CLIENTES_PEDIDO A
    /* Se elimina filtro para poder reenviar los clientes no importando que ya se hallan enviado
    WHERE NOT EXISTS (SELECT 1
                      FROM MCLIEN22F C WITH (NOLOCK)
                      WHERE C.COMPANIA = @COMPANIA
                      AND C.CLIENTE = A.clienteID
                      AND C.FECCREACIO = dbo.FC_INTEGERDATE(GETDATE())
                      AND C.TIPOINTE = 'C'
                      AND C.ESTAINTE = 'I')*/

    --SELECT @CTE_X_PEDI = COUNT(*) FROM #CLIENTES_PEDIDO
    SELECT @CTE_X_INTE = COUNT(*) FROM #CLIENTES_INTEGRA

    IF @CTE_X_INTE > 0
    BEGIN

        DECLARE @CODLETR CHAR(2)

        --Obtener codigo pais
        SELECT @CODLETR = B.CODLETR
        FROM MCOMPA1F A WITH (NOLOCK)
        INNER JOIN BUBIGE1F B WITH (NOLOCK) ON A.PAIS = B.PAIS
        WHERE A.COMPANIA = @COMPANIA

        INSERT INTO TPLINT1F ([FCREACION], [ESTADO], [ROOTKEY], [SUCURSAL])
        VALUES (GETDATE(), 0, 'Clientes', @SUCURSAL)

        DECLARE @v_ID INT = 0;

        SELECT TOP 1 @v_ID = ID
        FROM TPLINT1F WITH (NOLOCK)
        WHERE ROOTKEY = 'Clientes'
          AND SUCURSAL = @SUCURSAL
        ORDER BY ID DESC;

        DECLARE @XmlCliente xml
        SET @XmlCliente = (
            SELECT 
                @COMPANIA AS compania,
                @v_ID AS idTableBM,
                -- Esto es para F2
                'CLIENTES' AS tipo,
                (
                SELECT
                    A.CLIENTE AS clienteID,
                    LTRIM(RTRIM(SUBSTRING(A.NOMCLIENTE, 1, 60))) AS nombre,
                    LTRIM(RTRIM(DIRDETCLCL)) AS direccion,
                    @CODLETR AS pais,
                    CAST(ISNULL(B.COORDY, 0.0) AS DECIMAL(18,6)) AS latitude,
                    CAST(ISNULL(B.COORDX, 0.0) AS DECIMAL(18,6)) AS longitude,
                    D.RUTA AS rutaID,
                    E.ZONADIST AS zonaID,
                    D.MODULO AS moduloID,
                    CONCAT(
                        CASE WHEN ISNULL(C.FLGLUNES, 'N') = 'S' THEN 'L' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGMARTES, 'N') = 'S' THEN 'M' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGMIERCOLES, 'N') = 'S' THEN 'R' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGJUEVES, 'N') = 'S' THEN 'J' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGVIERNES, 'N') = 'S' THEN 'V' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGSABADO, 'N') = 'S' THEN 'S' ELSE '' END,
                        CASE WHEN ISNULL(C.FLGDOMINGO, 'N') = 'S' THEN 'D' ELSE '' END
                    ) AS diasEnvio,
                    LTRIM(RTRIM(A.CANAL)) AS codigoCanal,
                    LTRIM(RTRIM(H.DESCRIPCION)) AS canal,
                    LTRIM(RTRIM(A.TLFCLIENTE)) AS telefono,
                    LTRIM(RTRIM(A.GIRONEGOCI)) AS codigoGiro,
                    LTRIM(RTRIM(I.GIRDNOM)) AS giro,
                    LTRIM(RTRIM(A.SUBGIROVS)) AS codigoSubGiro,
                    LTRIM(RTRIM(J.DESCSGIRO)) AS subGiro,
                    LTRIM(RTRIM(A.RUCCLIENTE)) AS RUC,
                    LTRIM(RTRIM(ISNULL(K.EMAIL, ''))) AS email
                FROM dbo.MCLIEN1F (NOLOCK) A
                LEFT OUTER JOIN dbo.MCLIEN4F (NOLOCK) B ON A.COMPANIA = ...
                B.COMPANIA AND A.SUCURSAL = B.SUCURSAL AND A.CLIENTE = B.CLIENTE
                LEFT OUTER JOIN dbo.MCLIEN11F (NOLOCK) C ON A.COMPANIA = 
                    C.COMPANIA AND A.CLIENTE = C.CLIENTE
                INNER JOIN dbo.MESTDI4F (NOLOCK) D ON A.COMPANIA = 
                    D.COMPANIA AND A.SUCURSAL = D.SUCURSAL AND B.MODULO = D.MODULO AND B.CODFVTA3 = D.CODFVTA3
                INNER JOIN dbo.MESTDI3F (NOLOCK) E ON A.COMPANIA = 
                    E.COMPANIA AND A.SUCURSAL = E.SUCURSAL AND D.RUTA = E.RUTA
                INNER JOIN dbo.MESTDI2F (NOLOCK) F ON A.COMPANIA = 
                    F.COMPANIA AND A.SUCURSAL = F.SUCURSAL AND E.ZONADIST = F.ZONADIST
                LEFT OUTER JOIN dbo.MPERSO1F (NOLOCK) G ON E.COMPANIA = 
                    G.COMPANIA AND E.VENDEDOR = G.PERSONA
                INNER JOIN dbo.TRELCONS1F (NOLOCK) T ON A.COMPANIA = 
                    T.COMPANIA AND A.SUBGIROVS = T.SUBGIRO
                INNER JOIN dbo.MCANDIST (NOLOCK) H ON A.COMPANIA = 
                    H.COMPANIA AND T.CANAL = H.CANAL
                INNER JOIN dbo.BGIRO1F (NOLOCK) I ON A.COMPANIA = 
                    I.COMPANIA AND T.GIRO = I.GIROEMPRES
                INNER JOIN dbo.BSGIRO1F (NOLOCK) J ON A.COMPANIA = 
                    J.COMPANIA AND A.SUBGIROVS = J.SUBGIRO
                INNER JOIN dbo.MPERSO1F (NOLOCK) K ON K.COMPANIA = 
                    A.COMPANIA AND K.PERSONA = A.CLIENTE
                INNER JOIN #CLIENTES_INTEGRA L ON A.CLIENTE = L.clienteID 
                    AND B.CODFVTA3 = L.CODFVTA3
                WHERE A.COMPANIA = @COMPANIA
                  AND A.SUCURSAL = @SUCURSAL
                FOR XML PATH ('cliente'), TYPE
                )
            FOR XML PATH (''), ROOT('clientes')
        )

        DECLARE @xmlcharCliente VARCHAR(MAX)
        SET @xmlcharCliente = CAST(@XmlCliente AS VARCHAR(MAX))

        UPDATE TPLINT1F
        SET DATA = @xmlcharCliente
        WHERE ID = @v_ID;

        -- Esto es para F2
        EXEC COM_PLINT_CONSUMO_AWS 'M', @COMPANIA, @SUCURSAL, @xmlcharCliente
        --EXEC COM_PLINT_CONSUMO_AWS 'C', @COMPANIA, @SUCURSAL, @xmlcharCliente

        -- Se inserta Registro de Log de Integración
        INSERT INTO MCLIEN22F
        SELECT @COMPANIA, clienteID, 'C', 'I', dbo.FC_INTEGERDATE(GETDATE()), 
            dbo.FC_HORA(GETDATE()), 'SYSTEM', dbo.FC_INTEGERDATE(GETDATE()), dbo.FC_HORA(GETDATE()), 
            'SYSTEM'
        FROM #CLIENTES_INTEGRA A
        WHERE NOT EXISTS (SELECT * FROM MCLIEN22F C WHERE C.COMPANIA = @COMPANIA AND 
            C.CLIENTE = A.clienteID AND C.TIPOINTE = 'C' AND C.FECCREACIO = 
            dbo.FC_INTEGERDATE(GETDATE()))

        -- Se actualiza registro de Integración Pendiente
        UPDATE A
        SET A.ESTAINTE = 'I'
        FROM MCLIEN22F A
        INNER JOIN #CLIENTES_INTEGRA B ON A.CLIENTE = B.clienteID
        AND A.ESTAINTE = 'P'
    END
------------------------------------------------------------------------------------------
--                                                             FIN INTEGRACION CLIENTES --
------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------
    -- SE REALIZA CAMBIO DE PROCEDURE PARA MANEJAR UN MAXIMO DE 1000 PEDIDOS - CLIENTE POR ENVIO,
    -- PARA EVITAR EL TAMAÑO MAXIMO DE DATA POR ENVIAR EN AWS
    ------------------------------------------------------------------------------------------
    
    SELECT ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS ROWNUM, a.COMPANIA, a.SUCURSAL, 
    a.CLIENTE, a.DOCUPEDIDO, a.NROPEDIDO
    INTO #DATA_PEDIDOS
    FROM DBO.TPGVEH1F (NOLOCK) a
        INNER JOIN #TMP_ZONAS c ON a.ZONADIST = c.ZONA
        INNER JOIN DBO.TPEDID1F (NOLOCK) d ON a.compania = d.compania and a.sucursal = 
    d.sucursal and a.docupedido = d.docupedido and a.nropedido = d.nropedido
    WHERE a.COMPANIA = @COMPANIA
        AND a.SUCURSAL = @SUCURSAL
        AND ISNULL(a.DOCUCOMALM, '')=''

    DECLARE @NTOTAL INT,
            @NITERA INT,
            @NIDX INT = 0,
            @OPSENVIO VARCHAR(500) = ''

    DECLARE @ID_LOTE INT ;

    SELECT @NTOTAL = COUNT(*) FROM #DATA_PEDIDOS
    SELECT @NITERA = @NTOTAL / 1000

    WHILE (@NIDX * 1000 < @NTOTAL)
    BEGIN

        --INSERTAR AL INBOX PARA GENERAR ID
        INSERT INTO TPLINT1F ([FCREACION], [ESTADO], [ROOTKEY], [SUCURSAL])
        VALUES (GETDATE(), 0, 'Pedidos', @SUCURSAL)

        -- OBTENEMOS EL ID CREADO
        SELECT TOP 1 @ID_LOTE = ID
        FROM TPLINT1F
        WHERE ROOTKEY = 'Pedidos'
            AND SUCURSAL = @SUCURSAL
        ORDER BY ID DESC --SET @ID_LOTE = isnull((SELECT top 1 ID_LOTE FROM TPGVEH2F 
    order by ID_LOTE desc),0) + 1

        SET @V_XML = (
            SELECT
                @COMPANIA AS compania,
                LTRIM(RTRIM(@SUCURSAL)) AS sucursal,
                @ID_LOTE AS idTableBM,
                (
                    SELECT
                        CONCAT(LTRIM(RTRIM(A.DOCUPEDIDO)), '-', 
                CAST(A.NROPEDIDO AS VARCHAR), '-', CAST(A.CLIENTE AS VARCHAR)) AS ID,
                        a.CLIENTE AS clienteID,
                        CAST((
                            SELECT
                                SUM(CAST(ISNULL(D.QCAJASIGP + 
                (D.QBOTASIGP / E.QCONTENIDO), 0) AS float)) AS cajas
                            FROM DBO.TPEDID2F (NOLOCK) D
                            INNER JOIN DBO.MARTIC1F (NOLOCK) E ON 
                D.COMPANIA = E.COMPANIA AND D.ARTICULO = E.ARTICULO
                            INNER JOIN MLINEA1F F WITH (NOLOCK) ON 
                E.COMPANIA = F.COMPANIA AND E.LINEA = F.LINEA AND F.FLGLINEA='Te'
                            WHERE D.COMPANIA = a.COMPANIA
                            AND D.SUCURSAL = a.SUCURSAL
                            AND D.DOCUPEDIDO = A.DOCUPEDIDO
                            AND D.NROPEDIDO = A.NROPEDIDO
                            AND D.CLIENTE = A.CLIENTE
                        ) AS varchar) AS cajas,
                        CAST((
                            SELECT
                                SUM(CAST(ISNULL(E.QPESO * 
                ISNULL(D.QCAJASIGP + (D.QBOTASIGP / E.QCONTENIDO), 0) ,0) AS float)) AS pesoTotal
                            FROM DBO.TPEDID2F (NOLOCK) D
                            INNER JOIN DBO.MARTIC1F (NOLOCK) E ON 
                D.COMPANIA = E.COMPANIA AND D.ARTICULO = E.ARTICULO
                            INNER JOIN MLINEA1F F WITH (NOLOCK) ON 
                E.COMPANIA = F.COMPANIA AND E.LINEA = F.LINEA AND F.FLGLINEA='Te'
                            WHERE D.COMPANIA = a.COMPANIA
                            AND D.SUCURSAL = a.SUCURSAL
                            AND D.DOCUPEDIDO = A.DOCUPEDIDO
                            AND D.NROPEDIDO = A.NROPEDIDO
                            AND D.CLIENTE = A.CLIENTE
                        ) AS varchar) AS peso,
                        CAST((
                            SELECT
                                SUM(CAST(ISNULL(E.QTOTAL * 
                ISNULL(D.QCAJASIGP * E.QCONTENIDO) + D.QBOTASIGP, 0), 0) AS float)) AS volumenTotal
                            FROM DBO.TPEDID2F (NOLOCK) D
                            INNER JOIN DBO.MARTIC1F (NOLOCK) E ON 
                D.COMPANIA = E.COMPANIA AND D.ARTICULO = E.ARTICULO
                            INNER JOIN MLINEA1F F WITH (NOLOCK) ON 
                E.COMPANIA = F.COMPANIA AND E.LINEA = F.LINEA AND F.FLGLINEA='Te'
                            WHERE D.COMPANIA = a.COMPANIA
                            AND D.SUCURSAL = a.SUCURSAL
                            AND D.DOCUPEDIDO = A.DOCUPEDIDO
                            AND D.NROPEDIDO = A.NROPEDIDO
                            AND D.CLIENTE = A.CLIENTE
                        ) AS varchar) AS volumen,
                        'Venta' as tipoPedido,
                        CASE WHEN ISNULL(d.FECENTREGA, 0) > 0 
                            THEN CONVERT(date, dbo.FC_FECHA(d.FECENTREGA))
                            ELSE CONVERT(date, DATEADD(DAY, +1, GETDATE()))
                        END AS fechaEnvio,
                        (
                            SELECT
                                CAST(D.ARTICULO AS VARCHAR) AS articuloID,
                                LTRIM(RTRIM(E.DESCRIPI1)) AS articuloDescripcion,
                                CAST(ISNULL(D.QCAJASIGP, 0) AS DECIMAL(10,0)) AS cajas,
                                CAST(ISNULL(D.QBOTASIGP, 0) AS DECIMAL(10,0)) AS unidades,
                                CAST(CAST(ISNULL(E.QPESO * 
                ISNULL(D.QCAJASIGP + (D.QBOTASIGP / E.QCONTENIDO), 0) ,0) AS float) AS VARCHAR) AS pesoTotal,
                                CAST(CAST(ISNULL(E.QTOTAL * 
                ISNULL(D.QCAJASIGP * E.QCONTENIDO) + D.QBOTASIGP, 0), 0) AS float) AS VARCHAR) AS volumenTotal,
                                CAST(CAST(ISNULL(E.QPESO * 
                ISNULL(D.QCAJASIGP + (D.QBOTASIGP / E.QCONTENIDO), 0) ,0) AS float) AS VARCHAR) AS peso,
                                CAST(CAST(ISNULL(E.QTOTAL * 
                ISNULL(D.QCAJASIGP * E.QCONTENIDO) + D.QBOTASIGP, 0), 0) AS float) AS VARCHAR) AS volumen,
                                CASE D.PROCPEDIDO WHEN '003' THEN 
                                'Venta' WHEN '006' THEN 'Bonificación' ELSE 'Por Procesar' END as procedimientoDescripcion,
                                CAST(ISNULL(E.QCONTENIDO, 0) AS DECIMAL(10,0)) AS qContenido,
                                CAST(ISNULL((D.QCAJASIGP * E.QCONTENIDO) + D.QBOTASIGP, 0) AS DECIMAL(10,0)) AS totalBotellas,
                                D.IDREGLA as codPromocion
                            FROM DBO.TPEDID2F D WITH (NOLOCK)
                            INNER JOIN DBO.MARTIC1F E WITH (NOLOCK) ON D.COMPANIA = E.COMPANIA AND D.ARTICULO = E.ARTICULO
                            INNER JOIN MLINEA1F F WITH (NOLOCK) ON E.COMPANIA = F.COMPANIA AND E.LINEA = F.LINEA AND F.FLGLINEA='Te'
                            WHERE D.COMPANIA = a.COMPANIA
                                AND D.SUCURSAL = a.SUCURSAL
                                AND D.DOCUPEDIDO = A.DOCUPEDIDO
                                AND D.NROPEDIDO = A.NROPEDIDO
                                AND D.CLIENTE = A.CLIENTE
                                AND (D.QCAJASIGP + (D.QBOTASIGP / E.QCONTENIDO)) > 0
                                -- Se omite validacion por procedimiento
                                --AND D.PROCPEDIDO IN ('003', '006')
                            ORDER BY D.IDREGLA, D.PROCPEDIDO
                            FOR XML path('pedidoDetalle'), type
                        )
                    FROM DBO.TPGVEH1F (NOLOCK) a
                    INNER JOIN #TMP_ZONAS c ON a.ZONADIST = c.ZONA
                    INNER JOIN DBO.TPEDID1F (NOLOCK) d ON a.compania = d.compania and a.sucursal = d.sucursal and a.docupedido = d.docupedido and a.nropedido = d.nropedido
                    INNER JOIN #DATA_PEDIDOS e ON a.COMPANIA = e.COMPANIA AND a.SUCURSAL = e.SUCURSAL and a.CLIENTE = e.CLIENTE and a.DOCUPEDIDO = e.DOCUPEDIDO and a.NROPEDIDO = e.NROPEDIDO
                    WHERE a.COMPANIA = @COMPANIA
                        AND a.SUCURSAL = @SUCURSAL
                        AND ISNULL(a.DOCUCOMALM, '') = ''
                        AND e.ROWNUM BETWEEN (@NIDX * 1000 + 1) AND (@NIDX * 1000 + 1000)
                        -- Se agrega filtrado para validar que no se agreguen cabeceras que no tienen detalles
                        AND EXISTS (SELECT 1 
                                    FROM dbo.TPEDID2F Z WITH (NOLOCK)
                                    INNER JOIN DBO.MARTIC1F Y WITH (NOLOCK) ON Z.COMPANIA = Y.COMPANIA AND Z.ARTICULO = Y.ARTICULO
                                    INNER JOIN dbo.MLINEA1F X WITH (NOLOCK) ON Y.COMPANIA = X.COMPANIA AND Y.LINEA = X.LINEA AND X.FLGLINEA = 'Te'
                                    WHERE Z.COMPANIA = A.COMPANIA
                                        AND Z.SUCURSAL = A.SUCURSAL
                                        AND Z.DOCUPEDIDO = A.DOCUPEDIDO
                                        AND Z.NROPEDIDO = A.NROPEDIDO
                                        AND Z.CLIENTE = A.CLIENTE
                                        AND (Z.QCAJASIGP + (Z.QBOTASIGP / Y.QCONTENIDO)) > 0
                                        -- Se omite validacion por procedimiento
                                        --AND Z.PROCPEDIDO IN ('003', '006')
                                    )
                    FOR XML path('pedido'), type
                )
            FROM DBO.TCOMPA2F (NOLOCK)
            WHERE COMPANIA=@COMPANIA AND SUCURSAL=@SUCURSAL
            FOR XML PATH ('pedidos'), type
        )
        SET @v_eXML = cast(@V_XML as varchar(max));    ---CONVERT(@V_XML, varchar(max));

        -- ACTUALIZAMOS EL REGISTRO CREADO CON LA DATA QUE SE ENVIA
        UPDATE TPLINT1F
        SET DATA = @v_eXML
        WHERE ROOTKEY = 'Pedidos' AND ID = @ID_LOTE
        AND SUCURSAL = @SUCURSAL

        EXEC [COM_PLINT_INTEGRATION_CONSUMO_AWS] 'ROADNET', @Pais, @COMPANIA, @ID_LOTE, @v_eXML;

        SET @OPSENVIO += CASE WHEN LEN(LTRIM(RTRIM(@OPSENVIO))) = 0 THEN '' ELSE ',' END + CAST(@ID_LOTE AS VARCHAR)

        SET @NIDX += 1
    END

    DECLARE @NCAJASPE FLOAT = 0,
            @NCAJASAS FLOAT = 0,
            @NPESO FLOAT = 0

    SELECT @NCAJASAS = SUM(B.QCAJASIGP + (B.QBOTASIGP / C.QCONTENIDO)),
           @NCAJASPE = SUM(B.QCAJPEDID + (B.QBOTPEDID / C.QCONTENIDO)),
           @NPESO = SUM(C.QPESO * ISNULL(B.QCAJASIGP + (B.QBOTASIGP / C.QCONTENIDO), 0))
    FROM #DATA_PEDIDOS A WITH (NOLOCK)
        INNER JOIN TPEDID2F B WITH (NOLOCK) ON A.COMPANIA = B.COMPANIA AND A.SUCURSAL = 
    B.SUCURSAL AND A.DOCUPEDIDO = B.DOCUPEDIDO AND A.NROPEDIDO = B.NROPEDIDO
        AND A.CLIENTE = B.CLIENTE
        INNER JOIN MARTIC1F C WITH (NOLOCK) ON A.COMPANIA = C.COMPANIA AND B.ARTICULO = 
    C.ARTICULO
        INNER JOIN MLINEA1F F WITH (NOLOCK) ON C.COMPANIA = F.COMPANIA AND C.LINEA = 
    F.LINEA AND F.FLGLINEA='Te'

    -- SETEAMOS VALORES DE BITACORA
    UPDATE TPLINT3F
    SET OPSENVIO = @OPSENVIO,
        NPEDIDEN = @NTOTAL,
        NCAJASPE = @NCAJASPE,
        NCAJASAS = @NCAJASAS,
        NPESO = @NPESO
    WHERE COMPANIA = @COMPANIA
        AND SUCURSAL = @SUCURSAL
        AND EMISOR = @EMISOR
        AND ID = @ID

END

```