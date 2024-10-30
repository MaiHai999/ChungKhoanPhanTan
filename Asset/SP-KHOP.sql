


--CREATE PROCEDURE SP_KHOPLENH_LO
--    @macp NVARCHAR(10),
--    @Ngay NVARCHAR(10),
--    @LoaiGD CHAR(1),
--    @soluongMB INT,
--    @giadatMB FLOAT,
--    @malenhMB INT
--AS
--BEGIN
--	BEGIN TRANSACTION;

--	BEGIN TRY
--		SET DATEFORMAT DMY
--		DECLARE @CrsrVar CURSOR , @ngaydat NVARCHAR( 10), @soluong INT, @giadat FLOAT,  @soluongkhop INT, @giakhop FLOAT,  @malenhdat INT, @phi FLOAT, @matknh NVARCHAR(50), @mandt INT;

--		 IF (@LoaiGD='B')
--		   EXEC CursorLoaiGD  @CrsrVar OUTPUT, @macp,@Ngay, 'M'
--		 ELSE 
--		  EXEC CursorLoaiGD  @CrsrVar OUTPUT, @macp,@Ngay, 'B'

--		-- VÒNG LẬP CON TRỎ
--		FETCH NEXT FROM @CrsrVar  INTO  @ngaydat , @soluong , @giadat , @malenhdat

--		WHILE (@@FETCH_STATUS <> -1 AND @soluongMB > 0)
--		BEGIN
--			IF @LoaiGD = 'B'
--			BEGIN
--				IF @giadatMB < @giadat
--				BEGIN 
--					IF @soluongMB > @soluong
--					BEGIN 
--						SET @soluongkhop = @soluong
--						SET @giakhop = @giadat
--						SET @soluongMB = @soluongMB - @soluong
--						-- CẬP NHẬT LẠI DÒNG VỪA TÌM
--						UPDATE dbo.LENHDAT  
--						  SET SOLUONG = 0,
--							  TRANGTHAI = 'KHOP HET'
--						  WHERE CURRENT OF @CrsrVar

--						-- CẬP NHẬT DONG CẦM ĐI KHỚP DÒNG KHÁC
--						UPDATE dbo.LENHDAT
--						SET SOLUONG = SOLUONG - @soluongMB,
--							TRANGTHAI = 'KHOP MOT PHAN'
--						WHERE ID = @malenhMB;

--					END
--					ELSE
--					BEGIN
--					  SET @soluongkhop = @soluongMB
--					  SET @giakhop = @giadat
			  
--					  -- CẬP NHẬT LẠI DÒNG VỪA TÌM
--					  UPDATE dbo.LENHDAT  
--						 SET SOLUONG = SOLUONG - @soluongMB,
--							 TRANGTHAI = 'KHOP MOT PHAN'
--						 WHERE CURRENT OF @CrsrVar

--					  -- CẬP NHẬT DONG CẦM ĐI KHỚP DÒNG KHÁC
--					  UPDATE dbo.LENHDAT
--					  SET SOLUONG = 0,
--						TRANGTHAI = 'KHOP HET'
--					  WHERE ID = @malenhMB;


--					  SET @soluongMB = 0
--					END

--						-- CẬP NHẬT BẢNG KHỚP LỆNH
--						SET @phi = (@soluongkhop * @giakhop) * 0.03;
--						INSERT INTO [dbo].[LENHKHOP] (NGAYKHOP,SOLUONGKHOP,GIAKHOP,PHI,MALENHDAT)
--						VALUES (GETDATE(), @soluongkhop, @giakhop,@phi,@malenhdat),
--							   (GETDATE(), @soluongkhop, @giakhop,@phi,@malenhMB);

--						-- CẬP NHẬT TÀI KHOẢN NGÂN HÀNG BÂN BÁN
--						SELECT @matknh = MATKNH FROM dbo.LENHDAT WHERE ID = @malenhMB;
--						UPDATE TAIKHOANNGANHANG SET SODU = (SODU +(@soluongkhop * @giakhop)) - @phi WHERE MATK = @matknh;

--						-- CẬP NHẬT SỞ HỮU CỔ PHIẾU BÊN BÁN
--						SELECT @mandt = IDNDT FROM dbo.TAIKHOANNGANHANG WHERE MATK = @matknh;
--						UPDATE SOHUUCOPHIEU SET SOLUONG = SOLUONG - @soluongkhop WHERE MANDT = @mandt AND MACP = @macp;


--						-- CẬP NHẬT TÀI KHOẢN NGÂN HÀNG BÂN MUA
--						SELECT @matknh = MATKNH FROM dbo.LENHDAT WHERE ID = @malenhdat;
--						UPDATE TAIKHOANNGANHANG SET SODU = (SODU - (@soluongkhop * @giakhop)) - @phi WHERE MATK = @matknh;

--						-- CẬP NHẬT SỞ HỮU CỔ PHIẾU BÊN MUA
--						SELECT @mandt = IDNDT FROM dbo.TAIKHOANNGANHANG WHERE MATK = @matknh;
--						UPDATE SOHUUCOPHIEU SET SOLUONG = SOLUONG + @soluongkhop WHERE MANDT = @mandt AND MACP = @macp;

--				END
--			END
--			ELSE
--			BEGIN 
--				IF @giadatMB >= @giadat
--				BEGIN 
--					IF @soluongMB > @soluong
--					BEGIN 
--						SET @soluongkhop = @soluong
--						SET @giakhop = @giadat
--						SET @soluongMB = @soluongMB - @soluong
--						-- CẬP NHẬT LẠI DÒNG VỪA TÌM
--						UPDATE dbo.LENHDAT  
--							SET SOLUONG = 0,
--								TRANGTHAI = 'KHOP HET'
--							WHERE CURRENT OF @CrsrVar

--						-- CẬP NHẬT DONG CẦM ĐI KHỚP DÒNG KHÁC
--						UPDATE dbo.LENHDAT
--						SET SOLUONG = SOLUONG - @soluongMB,
--							 TRANGTHAI = CASE 
--											WHEN SOLUONG - @soluongMB <= 0 THEN 'KHOP HET'
--											ELSE 'KHOP MOT PHAN'
--										 END
--						WHERE ID = @malenhMB;

--					END
--					ELSE
--					BEGIN
--						SET @soluongkhop = @soluongMB
--						SET @giakhop = @giadat
			  
--						-- CẬP NHẬT LẠI DÒNG VỪA TÌM
--						UPDATE dbo.LENHDAT  
--							SET SOLUONG = SOLUONG - @soluongMB,
--								TRANGTHAI = CASE 
--												WHEN SOLUONG - @soluongMB <= 0 THEN 'KHOP HET'
--												ELSE 'KHOP MOT PHAN'
--											END
--							WHERE CURRENT OF @CrsrVar

--						-- CẬP NHẬT DONG CẦM ĐI KHỚP DÒNG KHÁC
--						UPDATE dbo.LENHDAT
--						SET SOLUONG = 0,
--						TRANGTHAI = 'KHOP HET'
--						WHERE ID = @malenhMB;


--						SET @soluongMB = 0
--					END

--					-- CẬP NHẬT BẢNG KHỚP LỆNH
--					SET @phi = (@soluongkhop * @giakhop) * 0.03;
--					INSERT INTO [dbo].[LENHKHOP] (NGAYKHOP,SOLUONGKHOP,GIAKHOP,PHI,MALENHDAT)
--					VALUES (GETDATE(), @soluongkhop, @giakhop,@phi,@malenhdat),
--							(GETDATE(), @soluongkhop, @giakhop,@phi,@malenhMB);

--					-- CẬP NHẬT TÀI KHOẢN NGÂN HÀNG BÂN MUA
--					SELECT @matknh = MATKNH FROM dbo.LENHDAT WHERE ID = @malenhMB;
--					UPDATE TAIKHOANNGANHANG SET SODU = (SODU -(@soluongkhop * @giakhop)) - @phi WHERE MATK = @matknh;

--					-- CẬP NHẬT SỞ HỮU CỔ PHIẾU BÊN MUA
--					SELECT @mandt = IDNDT FROM dbo.TAIKHOANNGANHANG WHERE MATK = @matknh;
--					UPDATE SOHUUCOPHIEU SET SOLUONG = SOLUONG + @soluongkhop WHERE MANDT = @mandt AND MACP = @macp;

--					-- CẬP NHẬT TÀI KHOẢN NGÂN HÀNG BÂN BÁN
--					SELECT @matknh = MATKNH FROM dbo.LENHDAT WHERE ID = @malenhdat;
--					UPDATE TAIKHOANNGANHANG SET SODU = (SODU + (@soluongkhop * @giakhop)) - @phi WHERE MATK = @matknh;

--					-- CẬP NHẬT SỞ HỮU CỔ PHIẾU BÊN BÁN
--					SELECT @mandt = IDNDT FROM dbo.TAIKHOANNGANHANG WHERE MATK = @matknh;
--					UPDATE SOHUUCOPHIEU SET SOLUONG = SOLUONG - @soluongkhop WHERE MANDT = @mandt AND MACP = @macp;

--				END

--			END
    
    
--			-- Lấy dữ liệu tiếp theo
--			FETCH NEXT FROM @CrsrVar INTO @ngaydat, @soluong, @giadat, @malenhdat;
--		END

--		-- ĐÓNG VÀ HỦY CON TRỎ
--		CLOSE @CrsrVar
--		DEALLOCATE @CrsrVar

--		-- Commit nếu không có lỗi
--		COMMIT TRANSACTION;
--	END TRY
--	BEGIN CATCH
--		-- Rollback nếu có lỗi
--		ROLLBACK TRANSACTION;

--		-- Thông báo lỗi
--		PRINT 'Có lỗi xảy ra: ' + ERROR_MESSAGE();
--	END CATCH;
--END










CREATE TRIGGER TG_KHOPLENH
ON LENHDAT
AFTER INSERT
AS
BEGIN
	DECLARE @matknh NVARCHAR(15), @macp NVARCHAR(6),@loailenh NVARCHAR(15), 
			@loaigd NVARCHAR(15), @soluong INT, @trangthai NVARCHAR(20),   
			@ngaydatlenh DATETIME, @gia FLOAT, @id INT;
	 SELECT 
        @matknh = MATKNH, @macp = MACP, @loailenh = LOAILENH,
        @loaigd = LOAIGD,@soluong = SOLUONG,@trangthai = TRANGTHAI,
        @ngaydatlenh = NGAYDATLENH,@gia = GIA, @id = ID
    FROM INSERTED;


	DECLARE @ngay1 NVARCHAR(10) = CONVERT(NVARCHAR(10), @ngaydatlenh, 103);

	IF @loailenh = 'LO'
	BEGIN
		EXECUTE SP_KHOPLENH_LO 
			@macp = @macp, 
			@Ngay = @ngay1,
			@LoaiGD = @loaigd, 
			@soluongMB = @soluong, 
			@giadatMB = @gia, 
			@malenhMB = @id; 
	END

END;






