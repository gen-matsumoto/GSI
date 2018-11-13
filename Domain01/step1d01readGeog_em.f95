! ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80
!$ ncdump -h geo_em.d02.nc 
!   Refer to ./ncdump.txt
! ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80
program read_geog_em
  implicit none
  include 'netcdf.inc'

  integer, parameter :: &
!       nx=60, ny=55, nt=1           ! Domain02
       nx=69, ny=49, nt=1           ! Domain01
  integer       :: ncid, ier, rhid
  integer       :: temp_lm(nx,ny,nt), temp_lu(nx,ny,nt)! 
  real          :: temp_lon(nx,ny)  ! 
  real          :: temp_lat(nx,ny)  ! 
  character(60) :: inFile, outFile
  character(30) :: varx, vary, var1, var2
  integer :: i,j,k

  varx='CLONG'
  vary='CLAT'
  var1='LANDMASK'
  var2='LU_INDEX' ! Variable which want to get date form netCDF

  !inFile  = '../Input/geo_em.d02.nc'          ! Domain02
  !outFile = '../Output/lu_lmbefore.txt'
  inFile  = '../../Input/geo_em.d01.nc'          ! Domain01
  outFile = '../../Output/lu_lmd01.txt'
  !filename='../../../../DataForCal/input_data/OSTIA/2014/0614.nc'
  ! Open the file & Obtain NetCDF ID(ncid)
  ier = nf_open(inFile, nf_nowrite, ncid)
  if (ier /= 0) stop 'can not read ncid'

  ier = nf_inq_varid(ncid, var1, rhid)            ! Obtain var: LANDMASK
  if (ier /= 0) stop 'can not read varid'
  ier = nf_get_var_int(ncid, rhid, temp_lm)         ! Put data to 3rd argument
  if (ier /= 0) stop 'can not read data'

  ier = nf_inq_varid(ncid, var2, rhid)            ! Obatain var: LU_INDEX
  if (ier /= 0) stop 'can not read varid'
  ier = nf_get_var_int(ncid, rhid, temp_lu)         ! Put data 3rd argument
  if (ier /= 0) stop 'can not read data'

  ier = nf_inq_varid(ncid, varx, rhid)           ! Obtain varx: longitude
  ier = nf_get_var_real(ncid, rhid, temp_lon)!
  if (ier /= 0) stop 'can not read longtitude'

  ier = nf_inq_varid(ncid, vary, rhid)           ! Obtain vary: latitude
  ier = nf_get_var_real(ncid, rhid, temp_lat)!
  if (ier /= 0) stop 'can not read latitude'

  ier = nf_close(ncid)                           ! Claose NetCDF file
  !write(*,*) "netCDF is completely read"


  call dispArray(outFile, nx, ny, temp_lu, temp_lm, temp_lon, temp_lat) ! Output data obtained

end program read_geog_em

!----------------------------------------------------------------------
subroutine dispArray (fileName, nlon, nlat, value0, value1, value2, value3)
  implicit none

  ! --- intent ---
  character(60), intent(in) :: fileName
  integer, intent(in) :: nlon, nlat
  integer, intent(in) :: value0(nlon,nlat,1), value1(nlon,nlat,1)
  real   , intent(in) :: value2(nlon,nlat), value3(nlon,nlat)

  ! --- Variable ---
  integer             :: i, j
  real                :: lon(nlon), lat(nlat)

  ! --------------------------------------------------------- Open, Write, Close
  open(unit=7, File=trim(fileName))
  do j=1,nlat
     do i=1,nlon
        write(7,*) i,j, value2(i,j), value3(i,j), value0(i,j,1), value1(i,j,1)
     end do
  end do
  close(unit=7)
  return
end subroutine dispArray
