
subroutine setprob

    !> Copy this file to your directory and modify to set up problem
    !! parameters or read other data.
    !!
    !! This default version is for Boussinesq terms
    !! Eventually reading these should be moved into bouss_module

    use amr_module
    use bouss_module, only: startWithBouss, numSWEsteps,alpha
    implicit none
    integer iunit,i
    character(len=25) fname
    real(kind=8) :: ampl

#ifdef WHERE_AM_I
    write(6,*) 'starting setprob'
#endif
    write(6,*) '+++starting setprob'

    iunit = 7
    fname = 'setprob.data'
!   # open the unit with new routine from Clawpack 4.4 to skip over
!   # comment lines starting with #:
    call opendatafile(iunit, fname)

    read(7,*) minLevelBouss
    read(7,*) maxLevelBouss
    read(7,*) deepBouss
    read(7,*) isolver
    read(7,*) ibouss
    read(7,*) alpha
    read(7,*) startWithBouss
    read(7,*) numSWEsteps

    write(*,900) minLevelBouss, maxLevelBouss
    write(outunit,900) minLevelBouss, maxLevelBouss
 900 format("==> Applying Bouss equations to selected grids between levels ",i3," and ",i3)

    write(*,*)"==> Use Bouss. in water deeper than ",deepBouss
    write(outunit,*)"==> Use Bouss. in water deeper than ",deepBouss

    if (isolver .eq. 1) then
       write(*,*)" Using GMRES solver"
       write(outunit,*)" Using GMRES solver"
    else if (isolver .eq. 2) then
       write(*,*)" Using Pardiso solver"
       write(outunit,*)" Using Pardiso solver"
       !write(*,*)"Cannot use expired Pardiso solver"
       !write(outunit,*)"Cannot use expired Pardiso solver"
       !stop
    else if (isolver .eq. 3) then
#ifdef HAVE_PETSC
       write(*,*)"Using a PETSc solver"
       write(outunit,*)"Using PETSc solver"
#else
       write(*,*)"need to install PETSc for this option"
       stop
#endif
    else
       write(*,*)"Unknown solver",isolver," choose 1,2 or 3"
       write(outunit,*)"Unknown solver",isolver," choose 1,2 or 3"
       stop
    endif
    close(unit=iunit)

    if (ibouss .eq. 1) then
       write(*,*)" Using Madsen Schaeter equations"
       write(outunit,*)" Using Madsen Schaeter equations"
    else if (ibouss .eq. 2) then
       write(*,*)" Using SGN equations"
       write(outunit,*)" Using SGN equations"
    else
       write(*,*)" Unrecognized option for equation set"
       write(outunit,*)" Unrecognized option for equation set"
       stop
    endif

    write(*,*) "For SGN equations Alpha = ",alpha
    write(outunit,*) "For SGN equations Alpha = ",alpha

    if (.not. startWithBouss) then
       write(*,*)"==> Wait for ",numSWEsteps," full level 1 SWE steps before starting Bouss"
       write(outunit,*)"==> Wait for ",numSWEsteps," full level 1 SWE steps before starting Bouss"
    else
       write(*,*)"Using Bouss equations from the start"
       write(outunit,*)"Using Bouss equations from the start"
    endif

    close(unit=iunit)

#ifdef WHERE_AM_I
    write(6,*) 'ending   setprob'
#endif

end subroutine setprob
