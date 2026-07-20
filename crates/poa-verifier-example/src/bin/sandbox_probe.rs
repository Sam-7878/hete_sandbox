#[cfg(target_os = "openbsd")]
fn main() -> std::io::Result<()> {
    use std::ffi::CString;
    use std::fs;
    use std::process::Command;

    unsafe extern "C" {
        fn unveil(path: *const libc::c_char, permissions: *const libc::c_char) -> libc::c_int;
        fn pledge(promises: *const libc::c_char, execpromises: *const libc::c_char) -> libc::c_int;
    }
    fn c(value: &str) -> CString {
        CString::new(value).unwrap()
    }
    fn call_unveil(path: Option<&str>, permissions: Option<&str>) -> i32 {
        let p = path.map(c);
        let perms = permissions.map(c);
        unsafe {
            unveil(
                p.as_ref().map_or(std::ptr::null(), |v| v.as_ptr()),
                perms.as_ref().map_or(std::ptr::null(), |v| v.as_ptr()),
            )
        }
    }
    fn call_pledge(promises: &str) -> i32 {
        unsafe { pledge(c(promises).as_ptr(), std::ptr::null()) }
    }

    let scenario = std::env::args().nth(1).unwrap_or_default();
    fs::create_dir_all("/var/hete/audit")?;
    let probe = "/var/hete/audit/sandbox-probe.txt";
    fs::write(probe, "before-lock")?;
    if call_unveil(Some("/var/hete/audit"), Some("rwc")) != 0 {
        return Err(std::io::Error::last_os_error());
    }
    if call_unveil(None, None) != 0 {
        return Err(std::io::Error::last_os_error());
    }

    match scenario.as_str() {
        "allowed-path" => {
            if call_pledge("stdio rpath wpath cpath") != 0 {
                return Err(std::io::Error::last_os_error());
            }
            fs::write(probe, "allowed")?;
            println!("ALLOWED_PATH {}", fs::read_to_string(probe)?);
        }
        "denied-path" => {
            if call_pledge("stdio rpath") != 0 {
                return Err(std::io::Error::last_os_error());
            }
            match fs::read_to_string("/etc/passwd") {
                Ok(_) => {
                    eprintln!("DENIED_PATH_UNEXPECTEDLY_ALLOWED");
                    std::process::exit(70);
                }
                Err(error) => {
                    println!("DENIED_PATH errno={:?} error={error}", error.raw_os_error())
                }
            }
        }
        "prohibited-exec" => {
            if call_pledge("stdio") != 0 {
                return Err(std::io::Error::last_os_error());
            }
            let _ = Command::new("/bin/echo").arg("must-not-run").status();
            eprintln!("PROHIBITED_EXEC_UNEXPECTEDLY_SURVIVED");
            std::process::exit(71);
        }
        "post-lock-unveil" => {
            // Isolate unveil-lock behavior from pledge. Applying pledge("stdio")
            // first would terminate on the unveil syscall itself and would not
            // demonstrate the post-lock EPERM result.
            let rc = call_unveil(Some("/tmp"), Some("r"));
            if rc == 0 {
                eprintln!("POST_LOCK_UNVEIL_UNEXPECTEDLY_ALLOWED");
                std::process::exit(72);
            }
            println!(
                "POST_LOCK_UNVEIL_DENIED errno={:?}",
                std::io::Error::last_os_error().raw_os_error()
            );
        }
        _ => {
            eprintln!(
                "usage: sandbox_probe allowed-path|denied-path|prohibited-exec|post-lock-unveil"
            );
            std::process::exit(64);
        }
    }
    Ok(())
}

#[cfg(not(target_os = "openbsd"))]
fn main() {
    eprintln!("sandbox_probe is OpenBSD-only and produces no evidence on this platform");
    std::process::exit(69);
}
