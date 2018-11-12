! ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80
!$ ncdump -h geo_em.d02.nc 
!   ./Input/ncdump.txtを参照
! ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80
program d01_overWrite
  use netcdf
  implicit none

  integer, parameter  :: &
       ny = 49, nx = 69, lc = 33, nt = 1                 ! Dimension of Domain01

  character (len = 60) :: inFile
  character (len = 30) :: varx, vary, varLU, varLC
  integer :: ncid, varid, varlu_index, varlandusef
  integer :: ndims_in, nvars_in, ngatts_in, unlimdimid_in

  real :: lats_in(nx,ny), lons_in(nx,ny)   ! lat lon coordinate netCDF variables
  real :: LU_in(nx,ny,nt), LU_out(nx,ny,nt)

  integer    :: i,j,k
  integer    :: LU_INDEX(nx,ny)
  real       :: LANDUSEF(nx,ny,lc)
  real       :: lon, lat, val, val33(lc)

  ! ----------------------------------------- File name, variables to get values
  inFile = "../Input/geo_em.d01.nc"          ! Domain01
  varLU  = "LU_INDEX"
  varLC  = "LANDUSEF"
  
  ! ----------------------------------------- Open the file, and query the file.
  call check( nf90_open(inFile, nf90_write, ncid) )
  call check( nf90_inquire(ncid, ndims_in, nvars_in, ngatts_in, unlimdimid_in) )
  if (ndims_in /= 10 .or. unlimdimid_in /= 1) stop 0

  ! --------------------------------------------------------------------- Get id
  call check( nf90_inq_varid(ncid, varLU, varlu_index) )              ! LU_INDEX
  call check( nf90_inq_varid(ncid, varLC, varlandusef) )              ! LANDUSEF
  
  ! ----------------------------------------------- Chage valuse as for LU_INDEX
  open(unit=8,file='../Output/gsid01_luindex.txt', status='old')       ! Domain01
  do j=1,ny
     do i=1,nx
        read(8,*) lon, lat, val
        LU_INDEX(i,j) = int(val)
     end do
  end do
  close(unit=8)

  call check( nf90_put_var(ncid, varlu_index, LU_INDEX) )              ! Rewrite

  ! ---------------------------------------------- Change values as for LANDUSEF
  open(unit=8,file='../Output/gsid01_landusef.txt', status='old')      ! Domain01
  do j=1,ny
     do i=1,nx
        read(8,*) lon, lat, val33(1:lc)
        !print *, val33
        LANDUSEF(i,j,1:33) = val33
        !print *, A(i,j,1:lc)
     end do
  end do
  close(unit=8)

  call check( nf90_put_var(ncid, varlandusef, LANDUSEF) )              ! Rewrite

  ! ------------------------------------------------------------- Close the file
  call check( nf90_close(ncid) )

  ! If we got this far, everything worked as expected. Yipee! 
  print *,"*** SUCCESS reading example file sfc_pres_temp.nc!"

contains
  subroutine check(status)
    integer, intent ( in) :: status

    if(status /= nf90_noerr) then 
       print *, trim(nf90_strerror(status))
       stop "Stopped"
    end if
  end subroutine check
end program d01_overWrite

